import time
import argparse
from scraper import OJSScraper
from sources import sources


def run_scraper(selected_source=None):
    start_time = time.time()
    print("Starting scraping process...\n")

    for name, url in sources.items():
        if selected_source and name != selected_source:
            continue  # skip other sources

        print(f"[START] Scraping: {name.upper()}")
        scraper = OJSScraper(base_url=url, name=name)
        scraper.run()
        print(f"[DONE] Finished: {name.upper()}\n")

    end_time = time.time()
    duration = end_time - start_time
    minutes, seconds = divmod(duration, 60)
    print(f"Finished all in {int(minutes)} minutes {seconds:.2f} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OJS journal scraper.")
    parser.add_argument(
        "source",
        nargs="?",
        help="Optional: specify a campus key to scrape only one (e.g. stikvinc, ukdc)"
    )
    args = parser.parse_args()

    if args.source and args.source not in sources:
        print(f"[ERROR] '{args.source}' is not a valid source key.")
        print("Available keys:", ', '.join(sources.keys()))
    else:
        run_scraper(selected_source=args.source)
