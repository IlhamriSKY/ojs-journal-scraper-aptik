# Open Journal Systems (OJS) Scraper Starter Kit

This is a Python-based starter kit for scraping academic journal websites powered by Open Journal Systems (OJS). It supports both OAI-PMH and HTML scraping, with examples from several university journal websites, particularly from APTIK members, making it easy to adapt, extend, and customize for similar platforms or research purposes.

## 🧰 Python Version

Python 3.8 or higher is recommended.

## 📦 Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```

## 💾 MySQL Database Schema

Run this SQL script in your MySQL server:

```sql
CREATE DATABASE IF NOT EXISTS ojs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ojs;

CREATE TABLE journals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  cover_image_url TEXT,
  university VARCHAR(255),
  journal_url TEXT,
  status VARCHAR(50),
  created_at DATETIME,
  updated_at DATETIME,
  deleted_at DATETIME DEFAULT NULL
);

CREATE TABLE articles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  journal_id INT,
  title TEXT,
  authors TEXT,
  abstract TEXT,
  article_url TEXT,
  doi TEXT,
  university VARCHAR(255),
  status VARCHAR(50),
  created_at DATETIME,
  updated_at DATETIME,
  deleted_at DATETIME DEFAULT NULL,
  FOREIGN KEY (journal_id) REFERENCES journals(id)
);
```

## 🚀 Usage

1.  Create a `.env` file with your MySQL credentials:
    
    ```python
    DB_HOST=localhost
    DB_NAME=ojs
    DB_USER=remote
    DB_PASSWORD=yourpassword
    ```
    
2.  Run the scraper:
    
    ```bash
    python app.py
    ```
    
3.  Or run the scraper for a specific campus (source key):

    ```bash
    python app.py scu ukdc
    ```

    Replace `scu` with one of the available keys, for example: `ukdc`, `unpar`, `uwdp`, etc.

    ```bash
    python app.py --list
    ```

    For get all sources

## 🏫 Supported Universities

*   **UNPAR**: [https://journal.unpar.ac.id/](https://journal.unpar.ac.id/)
*   **UAJ**: [https://ejournal.atmajaya.ac.id/ejournalland/public/](https://ejournal.atmajaya.ac.id/ejournalland/public/)
*   **UKWMS**: [https://journal.ukwms.ac.id/](https://journal.ukwms.ac.id/)
*   **SCU**: [https://journal.unika.ac.id/](https://journal.unika.ac.id/)
*   **UAJY**: [https://ojs.uajy.ac.id/](https://ojs.uajy.ac.id/)
*   **USD**: [https://e-journal.usd.ac.id/](https://e-journal.usd.ac.id/)
*   **UNWIRA**: [https://journal.unwira.ac.id/](https://journal.unwira.ac.id/) _(⚠️ Blocked by Cloudflare)_
*   **Unika St. Thomas Medan**: [https://ejournal.ust.ac.id/](https://ejournal.ust.ac.id/)
*   **UWDP**: [https://journal.widyadharma.ac.id/](https://journal.widyadharma.ac.id/)
*   **UKDC**: [https://jurnal.ukdc.ac.id/](https://jurnal.ukdc.ac.id/)
*   **STIKVINC**: [https://journal.stikvinc.ac.id/index.php/jpk](https://journal.stikvinc.ac.id/index.php/jpk)
*   **STIK Sint Carolus**: [https://jurnal.stik-sintcarolus.ac.id/cjon](https://jurnal.stik-sintcarolus.ac.id/cjon)
*   **STIKES Elisabeth Medan**: [http://ejournal.stikeselisabethmedan.ac.id:85/index.php/EHJ/index](http://ejournal.stikeselisabethmedan.ac.id:85/index.php/EHJ/index)

## 📄 Add a new OJS source

You can add any source that supports OJS by editing the [sources.py](https://github.com/IlhamriSKY/ojs-journal-scraper-aptik/blob/main/sources.py) file

```python
    ("key", {
        "url": "website",
        "university": "Universitas Name"
    }),
```

Optionally, map its domain in `university_mapping` for proper university name resolution.