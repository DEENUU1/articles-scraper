from src.national_geographic import NationalGeographicScraper
from src.scraper import Context
import logging
from history import LocalVisitedOffers
from src.zaufana_3_strona import Zaufana3StronaScraper
from src.arjancodes import ArjanCodesScraper
from src.demagog import DemagogScraper
from src.notion import create_notion_page
from src.medium import MediumScraper
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_scraper(scraper, local_history):
    context = Context(scraper)
    parsed_offers = context.run_scraper()

    for offer in parsed_offers:
        logger.info(f"Found {offer.title} at {offer.url}")
        if local_history.check_if_url_exist(offer.url):
            logger.info(f"Offer {offer.url} already visited")
        else:
            local_history.add_url_to_file(offer.url)
            create_notion_page(
                offer.title,
                offer.url
            )


def main() -> None:
    local_history = LocalVisitedOffers()

    medium_scraper = MediumScraper(num_of_results=10)
    medium_scraper.url = "https://medium.com/search?q=python"

    national_geographic_scraper = NationalGeographicScraper(num_of_results=10)
    national_geographic_scraper.url = "https://www.nationalgeographic.com/science"

    zaufana_3_strona_scraper = Zaufana3StronaScraper(num_of_results=10)
    zaufana_3_strona_scraper.url = "https://zaufanatrzeciastrona.pl/"

    arjan_codes_scraper = ArjanCodesScraper(num_of_results=10)
    arjan_codes_scraper.url = "https://www.arjancodes.com/blog/"

    demagog_scraper = DemagogScraper(num_of_results=10)
    demagog_scraper.url = "https://demagog.org.pl/analizy_i_raporty/"

    scrapers = [
        medium_scraper, national_geographic_scraper, zaufana_3_strona_scraper, arjan_codes_scraper, demagog_scraper
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_scraper, scraper, local_history) for scraper in scrapers]

        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
