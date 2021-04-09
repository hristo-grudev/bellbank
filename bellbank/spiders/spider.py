import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import BellbankItem
from itemloaders.processors import TakeFirst


class BellbankSpider(scrapy.Spider):
	name = 'bellbank'
	start_urls = ['https://bell.bank//sxa/search/results/?s={6ACFD1D3-DE24-4732-ABC0-80A440C28D25}&itemid={9DF18270-703E-43A0-B5B0-34A64E48447E}&sig=&autoFireSearch=true&v=%7BF12AAE73-5194-4876-B0C3-A005BBF278A7%7D&p=999999&e=0']

	def parse(self, response):
		data = json.loads(response.text)

		for post in data['Results']:
			url = post['Url']
			yield response.follow(url, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="short-headline"]/text()').get()
		description = response.xpath('//div[@class="news-article"]//text()[normalize-space() and not(ancestor::div[@class="short-headline"] | ancestor::time)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=BellbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
