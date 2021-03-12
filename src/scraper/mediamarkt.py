from scraper.common import ScrapeResult, Scraper, ScraperFactory
import re

class MediaMarktScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        tag = self.soup.body.select_one('.gua-page-type-category')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        count = re.sub('[()]', '', tag.find('span').text.strip())

        if int(count) > 0:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class MediaMarktScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'mediamarkt'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return MediaMarktScrapeResult
