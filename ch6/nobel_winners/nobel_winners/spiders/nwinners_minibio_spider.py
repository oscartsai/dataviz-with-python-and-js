import scrapy
import re

BASE_URL = 'https://en.wikipedia.org'


class NWinnerItemBio(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()


class NWinnerSpiderBio(scrapy.Spider):
    """ Scrapes the Nobel prize biography pages for portrait images and a biographical snippet """

    name = 'nwinners_minibio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "http://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    # For Scrapy v 1.0+, custom_settings can override the item pipelines in settings
    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.NobelImagesPipeline':1},
    }

    def parse(self, response):

        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]

                    # print(wdata)
                    request = scrapy.Request(
                        wdata['link'],
                        callback=self.get_mini_bio,
                        dont_filter=True)

                    request.meta['item'] = NWinnerItemBio(**wdata)
                    yield request


    def get_mini_bio(self, response):
        """ Get the winner's bio-text and photo """

        item = response.meta['item']

        # Cache image
        item['image_urls'] = []
        # Get the URL of the winner's picture, contained in the infobox table
        img_src = response.xpath('//table[contains(@class, "infobox")]//img/@src')
        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()]

        mini_bio = ''
        # Get the paragraphs in the biography's body-text
        mwc = response.xpath('//*[@id="mw-content-text"]')
        paras = mwc.xpath('div/h2[1]/preceding-sibling::p')
        for p in paras[1:]:
            text = p.extract()
            text = re.sub(r'<.*?>', '', text)
            text = re.sub(r'\[\d+?\]', '', text)
            mini_bio += text
        item['mini_bio'] = mini_bio

        yield item
