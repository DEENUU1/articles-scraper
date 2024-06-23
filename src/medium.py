import time
from typing import Any, Optional, List

from selenium.common import TimeoutException

from src.article import Article
from src.scraper import ScraperStrategy
from src.utils import get_driver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.scroll import scroll_page_callback

logger = logging.getLogger(__name__)


class MediumScraper(ScraperStrategy):
    def __init__(self, num_of_results: int = 0):
        super().__init__()
        self.num_of_results = num_of_results

    def scrape(self) -> List[Article]:
        result = []
        fetched = set()
        driver = get_driver()
        driver.get(self.url)

        def click_show_more_button(driver):
            try:
                show_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show more')]"))
                )
                show_more_button.click()
                return True
            except TimeoutException:
                logger.error("Show more button not found or not clickable")
                return True
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return True

        def parse_article(article) -> Optional[Article]:
            try:
                url_element = article.find_element(By.XPATH, ".//a[@role='link']")
                title_element = article.find_element(By.TAG_NAME, "h2")

                url = url_element.get_attribute("href")
                title = title_element.text

                if not title or not url or url in fetched:
                    return None

                fetched.add(url)

                return Article(
                    url=url,
                    title=title,
                )
            except Exception as e:
                logger.error(f"An error occurred while parsing article: {e}")
                return None

        while len(result) < self.num_of_results or self.num_of_results == 0:
            print(f"Number of results: {len(result)}")
            print(f"Number of visited: {driver.current_url}")
            articles = driver.find_elements(By.TAG_NAME, "article")
            new_articles_found = False

            for article in articles:
                parsed_article = parse_article(article)
                if parsed_article:
                    result.append(parsed_article)
                    new_articles_found = True

                if 0 < self.num_of_results == len(result):
                    break

            if not new_articles_found or (self.num_of_results > 0 and len(result) >= self.num_of_results):
                break

            if not click_show_more_button(driver):
                break

        driver.quit()
        return result
