from typing import Any, Optional, List

from src.article import Article
from src.scraper import ScraperStrategy
from src.utils import get_driver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(__name__)


class DemagogScraper(ScraperStrategy):
    def __init__(self, num_of_results: int = 0):
        super().__init__()
        self.num_of_results = num_of_results

    @staticmethod
    def _click_button_to_load_articles(driver) -> bool:
        logger.info("Clicking button to load articles")

        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dg-cta.dg-load-more"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            # button.click()
            return True
        except Exception as e:
            logger.error(e)
        return False

    @staticmethod
    def _parse_article(article: Any) -> Optional[Article]:
        try:
            header_container = article.find_element(By.CSS_SELECTOR, "div.dg-latest-analysis__title")

            url = header_container.find_element(By.TAG_NAME, "a").get_attribute("href")
            title = header_container.find_element(By.TAG_NAME, "a").text
            obj_ = Article(url=url, title=title)

            return obj_
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def _click_cookies_button(driver) -> None:
        logger.info("Clicking privacy settings button")
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#cn-accept-cookie"))
            )
            button.click()
        except Exception as e:
            logger.error(e)

    def scrape(self) -> List[Article]:
        logger.info("Scraping Demagog")

        driver = get_driver()
        driver.get(self.url)

        logger.info("Waiting for page to load")
        cookies_modal = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "span#cn-notice-buttons"
            ))
        )
        if cookies_modal:
            self._click_cookies_button(driver)

        result = []
        visited = set()

        while len(visited) < self.num_of_results or self.num_of_results == 0:
            articles_container = driver.find_element(By.CSS_SELECTOR, "div.row.dg-listing-tiles__items")

            articles = articles_container.find_elements(By.CSS_SELECTOR, "div.dg-latest-analysis__item")
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
        driver.quit()
        return result

