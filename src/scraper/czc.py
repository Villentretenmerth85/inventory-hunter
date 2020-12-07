import logging

from scraper.common import ScrapeResult, Scraper, ScraperFactory


class CzcScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.select_one('head > title')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            logging.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('span[itemprop=price]')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'

        # check for add to cart button
        tag = self.soup.body.select_one('button[class="btn btn-buy"]')
        if tag and 'přidat do košíku' in tag.span.text.lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class CzcScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'czc'

    @staticmethod
    def get_driver_type():
        return 'selenium'

    @staticmethod
    def get_result_type():
        return CzcScrapeResult

    @staticmethod
    def generate_short_name(url):
        parts = [i for i in url.path.split('/') if i]
        if parts:
            return parts[-1].replace('.htm', '')
