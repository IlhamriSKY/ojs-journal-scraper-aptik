import cloudscraper
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urlparse
from datetime import datetime
import re
from connection import Database
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OJSScraper:
    def __init__(self, name, config):
        self.source_name = name
        self.base_url = config["url"].rstrip('/')
        self.university = config["university"]
        self.db = Database()

        # SSL handling
        if not self.is_verify_ssl():
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.scraper = cloudscraper.create_scraper(ssl_context=context)
        else:
            self.scraper = cloudscraper.create_scraper()

        # Namespace OAI-PMH
        self.namespaces = {
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/"
        }

    def is_verify_ssl(self):
        # Only skip SSL verification for specific source
        return False if self.source_name == "ukwms" else True

    def run(self):
        if not self.db.connect():
            return

        print(f"-- START scraping: {self.source_name.upper()} --")

        # Special case for UKWMS, use base URL directly for OAI
        if self.source_name == 'ukwms':
            journal_names = self.get_journal_names()
            for journal in journal_names:
                try:
                    print(f"[INFO] Processing journal: {journal}")
                    journal_url = self.get_valid_journal_url(journal)
                    journal_data = self.get_journal_info(journal_url)
                    if journal_data:
                        journal_id = self.save_journal(journal_data)
                        oai_url = self.get_valid_oai_url(journal)
                        if oai_url:
                            article_count = self.fetch_articles(oai_url, journal_id, journal_data['university'])
                            print(f"[DONE] {article_count} articles from '{journal}'")
                        elif self.source_name == "stikvinc":
                            article_count = self.fetch_articles_no_oai(journal_url, journal_id, journal_data['university'])
                            print(f"[DONE] {article_count} articles from '{journal}' (no OAI)")
                        else:
                            print(f"[SKIP] OAI not available for '{journal}'")
                        self.db.commit()
                except Exception as e:
                    print(f"[ERROR] Failed to process '{journal}': {e}")
                    continue
            self.db.close()
            print(f"-- FINISHED scraping: {self.source_name.upper()} --")
            return

        # Default scraping mode for other institutions
        journal_names = self.get_journal_names()
        for journal in journal_names:
            try:
                print(f"[INFO] Processing journal: {journal}")
                journal_url = self.get_valid_journal_url(journal)
                journal_data = self.get_journal_info(journal_url)
                if journal_data:
                    journal_id = self.save_journal(journal_data)
                    oai_url = self.get_valid_oai_url(journal)
                    if oai_url:
                        article_count = self.fetch_articles(oai_url, journal_id, journal_data['university'])
                        print(f"[DONE] {article_count} articles from '{journal}'")
                    elif self.source_name == "stikvinc":
                        article_count = self.fetch_articles_no_oai(journal_url, journal_id, journal_data['university'])
                        print(f"[DONE] {article_count} articles from '{journal}' (no OAI)")
                    else:
                        print(f"[SKIP] OAI not available for '{journal}'")
                    self.db.commit()
            except Exception as e:
                print(f"[ERROR] Failed to process '{journal}': {e}")
                continue

        self.db.close()
        print(f"-- FINISHED scraping: {self.source_name.upper()} --")

    def get_journal_names(self):
        # Special handling for known fixed-path journals
        if self.source_name == "stikvinc":
            return ['jpk']
        
        try:
            resp = self.scraper.get(self.base_url, timeout=10, verify=self.is_verify_ssl())
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find_all('a', href=True)
            journal_names = set()
            for link in links:
                href = link['href']
                match = re.search(r'/index\.php/([a-zA-Z0-9_-]+)/?$', href)
                if match:
                    name = match.group(1)
                    if name.lower() != 'index' and not name.isdigit():
                        journal_names.add(name)
            if not journal_names:
                print(f"[INFO] No specific journal found, fallback to 'index'")
                return ['index']
            return sorted(journal_names)
        except Exception as e:
            print(f"[WARN] Unable to get journal list from {self.base_url}: {e}")
            return ['index']

    def get_valid_journal_url(self, journal):
        # Special case for stikvinc
        if self.source_name == "stikvinc":
            return "https://journal.stikvinc.ac.id/index.php/jpk"

        urls = [
            f"{self.base_url}/index.php/{journal}/index",
            f"{self.base_url}/index.php/{journal}"
        ]
        for url in urls:
            try:
                resp = self.scraper.get(url, timeout=10, verify=self.is_verify_ssl())
                if resp.status_code == 200:
                    return url
            except:
                continue
        raise Exception(f"Cannot access journal page for {journal}")

    def get_valid_oai_url(self, journal):
        if self.source_name == "stikvinc":
            return None  # Tidak ada OAI endpoint

        if self.source_name == "ukwms":
            oai_url = f"{self.base_url}/oai"
            try:
                resp = self.scraper.get(oai_url, timeout=10, verify=self.is_verify_ssl())
                if resp.status_code == 200:
                    return oai_url
            except:
                pass

        oai_url = f"{self.base_url}/index.php/{journal}/oai"
        try:
            resp = self.scraper.get(oai_url, timeout=10, verify=self.is_verify_ssl())
            if resp.status_code == 200:
                return oai_url
        except:
            pass
        return None

    def get_journal_info(self, journal_url):
        try:
            resp = self.scraper.get(journal_url, timeout=10, verify=self.is_verify_ssl())
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.find('title').text.strip()
            img_tag = soup.find('img')
            image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
            return {
                'title': title,
                'cover_image_url': image_url,
                'journal_url': journal_url,
                'university': self.university,
                'status': 'active'
            }
        except Exception as e:
            print(f"[WARN] Failed to get journal info from {journal_url}: {e}")
            return None

    def safe_get(self, elements):
        return elements[0].text.strip() if elements and elements[0].text else None

    def save_journal(self, journal):
        self.db.execute("SELECT id FROM journals WHERE journal_url = %s", (journal['journal_url'],))
        result = self.db.fetchone()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if result:
            journal_id = result[0]
            self.db.execute("""
                UPDATE journals SET title=%s, cover_image_url=%s, university=%s, status=%s, updated_at=%s
                WHERE id=%s
            """, (
                journal['title'],
                journal['cover_image_url'],
                journal['university'],
                journal['status'],
                now,
                journal_id
            ))
            return journal_id
        else:
            self.db.execute("""
                INSERT INTO journals (title, cover_image_url, university, journal_url, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                journal['title'],
                journal['cover_image_url'],
                journal['university'],
                journal['journal_url'],
                journal['status'],
                now,
                now
            ))
            return self.db.cursor.lastrowid

    def save_article(self, article):
        self.db.execute("SELECT id FROM articles WHERE article_url = %s", (article['article_url'],))
        result = self.db.fetchone()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if result:
            article_id = result[0]
            self.db.execute("""
                UPDATE articles SET title=%s, authors=%s, abstract=%s, doi=%s, university=%s, updated_at=%s
                WHERE id=%s
            """, (
                article['title'],
                article['authors'],
                article['abstract'],
                article['doi'],
                article['university'],
                now,
                article_id
            ))
        else:
            self.db.execute("""
                INSERT INTO articles
                (journal_id, title, authors, abstract, article_url, doi, university, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                article['journal_id'],
                article['title'],
                article['authors'],
                article['abstract'],
                article['article_url'],
                article['doi'],
                article['university'],
                now,
                now
            ))

    def fetch_articles(self, oai_url, journal_id, university):
        params = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
        total = 0
        while True:
            try:
                resp = self.scraper.get(oai_url, params=params, timeout=15, verify=self.is_verify_ssl())
                resp.raise_for_status()
                parser = etree.XMLParser(recover=True)
                root = etree.fromstring(resp.content, parser=parser)
                records = root.xpath(".//oai:record", namespaces=self.namespaces)
                for rec in records:
                    title = self.safe_get(rec.xpath(".//dc:title", namespaces=self.namespaces))
                    if not title:
                        continue
                    authors = self.safe_get(rec.xpath(".//dc:creator", namespaces=self.namespaces))
                    abstract = self.safe_get(rec.xpath(".//dc:description", namespaces=self.namespaces))
                    identifier_el = rec.xpath(".//dc:identifier", namespaces=self.namespaces)
                    article_url, doi = "", ""
                    for ide in identifier_el:
                        if ide.text:
                            text = ide.text.strip()
                            if "doi.org" in text:
                                doi = text
                            elif "/article/view/" in text:
                                article_url = text
                    self.save_article({
                        "journal_id": journal_id,
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "article_url": article_url,
                        "doi": doi,
                        "university": university
                    })
                    total += 1
                token_el = root.xpath(".//oai:resumptionToken", namespaces=self.namespaces)
                if not token_el or not token_el[0].text:
                    break
                params = {"verb": "ListRecords", "resumptionToken": token_el[0].text}
            except Exception as e:
                print(f"[WARN] Failed to fetch articles from {oai_url}: {e}")
                break
        return total

    def fetch_articles_no_oai(self, journal_url, journal_id, university):
        total = 0
        try:
            resp = self.scraper.get(journal_url, timeout=10, verify=self.is_verify_ssl())
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            articles = soup.select('div.obj_issue_toc div.article-summary, div.obj_issue_toc div.obj_article_summary')
            for article in articles:
                title_tag = article.find('a')
                if not title_tag:
                    continue
                article_title = title_tag.text.strip()
                article_url = title_tag['href']

                authors_tag = article.find('div', class_='authors')
                authors = authors_tag.text.strip() if authors_tag else None

                abstract = None
                try:
                    detail_resp = self.scraper.get(article_url, timeout=10, verify=self.is_verify_ssl())
                    detail_resp.raise_for_status()
                    detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
                    abstract_tag = detail_soup.find('section', class_='item abstract')
                    if abstract_tag:
                        abstract = abstract_tag.text.strip()
                except Exception as e:
                    print(f"[WARN] Gagal ambil abstrak: {e}")

                self.save_article({
                    "journal_id": journal_id,
                    "title": article_title,
                    "authors": authors,
                    "abstract": abstract,
                    "article_url": article_url,
                    "doi": None,
                    "university": university
                })
                total += 1

        except Exception as e:
            print(f"[WARN] Gagal akses halaman jurnal langsung: {e}")
        
        return total
