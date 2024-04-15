import scrapy


class BookstoscrapecomSpider(scrapy.Spider):
    name = "bookstoscrapecom"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for book in response.css('article.product_pod'):
            yield {
                'title': book.css('h3 > a::text').get(),
                'price': float(book.css('div.product_price > p.price_color::text').re_first(r'[\d.]+')),
                'availability': book.css('div.product_price > p.instock.availability::text').get()
            }

        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
