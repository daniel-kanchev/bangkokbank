import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bangkokbank.items import Article


class BangkokSpider(scrapy.Spider):
    name = 'bangkok'
    start_urls = ['https://www.bangkokbank.com/th-TH/About-Us/News-and-Media']

    def parse(self, response):
        links = response.xpath('//a[@title="ดูรายละเอียด"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//p[@class="text-large text-light pad-bot"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="text-default pad-bot"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="center-content editor"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
