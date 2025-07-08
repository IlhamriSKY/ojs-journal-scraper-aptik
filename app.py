import time
import argparse
from scraper import OJSScraper
from sources import sources

def run_scraper(selected_sources=None):
    start_time = time.time()
    print("Starting scraping process...\n")

    if selected_sources:
        invalid_keys = [key for key in selected_sources if key not in sources]
        if invalid_keys:
            print(f"[ERROR] Invalid source keys: {', '.join(invalid_keys)}")
            print("Available keys:", ', '.join(sources.keys()))
            return
        items = [(key, sources[key]) for key in selected_sources]
    else:
        items = sources.items()

    for name, config in items:
        print(f"[START] Scraping: {name.upper()}")
        scraper = OJSScraper(name=name, config=config)
        scraper.run()
        print(f"[DONE] Finished: {name.upper()}\n")

    minutes, seconds = divmod(time.time() - start_time, 60)
    print(f"Finished all in {int(minutes)} minutes {seconds:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OJS journal scraper.")
    parser.add_argument(
        "sources",
        nargs="*",
        help="Optional: specify one or more campus keys (e.g. stikvinc ukdc scu)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available campus keys"
    )
    args = parser.parse_args()

    if args.list:
        print("Available campus keys:")
        for key in sources.keys():
            print(f"- {key}")
    else:
        run_scraper(selected_sources=args.sources)
