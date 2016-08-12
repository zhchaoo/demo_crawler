import scrapy

from demo_crawler.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("section[id^='cat-list-section'] div.cat-item a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//div[@class="title-and-desc"]'):
            item = DmozItem()
            item['title'] = sel.xpath('a/div/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('div[@class="site-descr "]/text()').re('\w[^\n\r]*')
            yield item


    def parse_articles_follow_next_page(self, response):
        for article in response.xpath("//article"):
            item = DmozItem()
            yield item

        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield DmozItem(url, self.parse_articles_follow_next_page)
