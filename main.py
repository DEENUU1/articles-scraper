from src.national_geographic import NationalGeographicScraper
from src.scraper import Context
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main() -> None:
    national_geographic_scraper = NationalGeographicScraper(num_of_results=10)
    national_geographic_scraper.url = "https://www.nationalgeographic.com/science"

    context = Context(national_geographic_scraper)

    parsed_offers = context.run_scraper()
    logger.info(parsed_offers)


if __name__ == "__main__":
    main()
