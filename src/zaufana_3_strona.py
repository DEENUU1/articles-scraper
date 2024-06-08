from typing import Any, Optional, List

from src.article import Article
from src.scraper import ScraperStrategy
from src.utils import get_driver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(__name__)


class Zaufana3StronaScraper(ScraperStrategy):
    def __init__(self, num_of_results: int = 0):
        super().__init__()
        self.num_of_results = num_of_results

    @staticmethod
    def _click_button_to_load_articles(driver) -> bool:
        logger.info("Clicking button to load articles")

        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@load-more-articles='']"))
            )
            button.click()
            return True
        except Exception as e:
            logger.error(e)
        return False

    @staticmethod
    def _parse_article(article: Any) -> Optional[Article]:
        try:
            url = article.find_element(By.CSS_SELECTOR, "a.list-articles__box").get_attribute("href")
            title = article.find_element(By.TAG_NAME, "h2").text
            obj_ = Article(url=url, title=title)

            return obj_
        except Exception as e:
            logger.error(e)
            return None

    def scrape(self) -> List[Article]:
        logger.info("Scraping Zaufana 3 Strona")

        driver = get_driver()
        driver.get(self.url)

        logger.info("Waiting for page to load")

        result = []
        visited = set()

        while len(visited) < self.num_of_results or self.num_of_results == 0:
            article_container = driver.find_element(By.CSS_SELECTOR, "div.list-articles__inner")
            articles = article_container.find_elements(By.TAG_NAME, "li")
            logger.info(f"Found {len(articles)} articles")

            if not articles:
                break

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

            if self.num_of_results == 0 or len(visited) < self.num_of_results:
                if not self._click_button_to_load_articles(driver):
                    break

        logger.info(f"Parse {len(result)} articles")
        return result

