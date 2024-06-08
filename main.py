from src.national_geographic import NationalGeographicScraper
from src.scraper import Context
import logging
from history import LocalVisitedOffers
from src.zaufana_3_strona import Zaufana3StronaScraper
from src.arjancodes import ArjanCodesScraper
from src.demagog import DemagogScraper
from src.notion import create_notion_page


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main() -> None:
    local_history = LocalVisitedOffers()

    national_geographic_scraper = NationalGeographicScraper(num_of_results=10)
    national_geographic_scraper.url = "https://www.nationalgeographic.com/science"

    zaufana_3_strona_scraper = Zaufana3StronaScraper(num_of_results=10)
    zaufana_3_strona_scraper.url = "https://zaufanatrzeciastrona.pl/"

    arjan_codes_scraper = ArjanCodesScraper(num_of_results=10)
    arjan_codes_scraper.url = "https://www.arjancodes.com/blog/"

    demagog_scraper = DemagogScraper(num_of_results=10)
    demagog_scraper.url = "https://demagog.org.pl/analizy_i_raporty/"

    context = Context(national_geographic_scraper)

    parsed_offers = context.run_scraper()

    for offer in parsed_offers:
        if local_history.check_if_url_exist(offer.url):
            logger.info(f"Offer {offer.url} already visited")
        else:
            local_history.add_url_to_file(offer.url)
            create_notion_page(
                offer.title,
                offer.url
            )


if __name__ == "__main__":
    main()
