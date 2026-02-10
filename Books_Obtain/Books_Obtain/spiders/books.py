import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    def start_requests(self):
        for i in range(1, 51):
            yield scrapy.Request(f"https://books.toscrape.com/catalogue/page-{i}.html", callback = self.parse)

    def parse(self, response):
        books = response.css('.product_pod')
        for book in books:
            a_url = book.css('h3 a::attr(href)').get()
            new_url = response.urljoin(a_url)
            yield response.follow(new_url, callback = self.parse_detail)

    def parse_detail(self, response):
        pass