from typing import Any, Optional, List

from src.article import Article
from src.scraper import ScraperStrategy
from src.utils import get_driver
import logging
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)


class ArjanCodesScraper(ScraperStrategy):
    def __init__(self, num_of_results: int = 0):
        super().__init__()
        self.num_of_results = num_of_results

    @staticmethod
    def _parse_article(article: Any) -> Optional[Article]:
        try:
            url = article.find_element(By.TAG_NAME, "a").get_attribute("href")
            title = article.find_element(By.TAG_NAME, "h3").text
            obj_ = Article(url=url, title=title)

            return obj_
        except Exception as e:
            logger.error(e)
            return None

    def scrape(self) -> List[Article]:
        logger.info("Scraping ArjanCodes")

        driver = get_driver()
        driver.get(self.url)

        result = []
        visited = set()

        articles = driver.find_elements(By.CSS_SELECTOR, "li.group.backdrop-blur-lg.transition")
        logger.info(f"Found {len(articles)} articles")

        if not articles:
            return result

        for article in articles:
            if not article:
                continue

            parsed_article = self._parse_article(article)
            if not parsed_article:
                continue

            if parsed_article.url in visited:
                continue

            result.append(parsed_article)
            visited.add(parsed_article.url)

            if 0 < self.num_of_results == len(visited):
                break

        logger.info(f"Parse {len(result)} articles")
        return result

