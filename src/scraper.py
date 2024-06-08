
class ScraperStrategy:
    def __init__(self):
        self._url = ""

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def scrape(self) -> ...:
        pass


class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def run_scraper(self) -> ...:
        return self.strategy.scrape()
