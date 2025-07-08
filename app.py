import time
from scraper import OJSScraper
from sources import sources

def run_scraper():
    start_time = time.time()
    print("Memulai proses scraping...\n")

    for name, url in sources.items():
        print(f"[START] Mulai scraping: {name.upper()}")
        scraper = OJSScraper(base_url=url, name=name)
        scraper.run()
        print(f"[DONE] Selesai scraping: {name.upper()}\n")

    end_time = time.time()
    duration = end_time - start_time
    minutes, seconds = divmod(duration, 60)
    print(f"Selesai! Total waktu: {int(minutes)} menit {seconds:.2f} detik.")

if __name__ == "__main__":
    run_scraper()
