from time import sleep
import logging

logger = logging.getLogger(__name__)


def scroll_page_callback(driver, callback) -> None:
    """
    Scrolls the page to load more data from a website
    """
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        consecutive_scrolls = 0

        while consecutive_scrolls < 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                consecutive_scrolls += 1
            else:
                consecutive_scrolls = 0

            last_height = new_height

            callback(driver)

    except Exception as e:
        logger.error(f"Error occurred while scrolling: {e}")