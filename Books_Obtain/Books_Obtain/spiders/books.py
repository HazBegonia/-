import scrapy

from ..items import BooksObtainItem
import re


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.Request(f"https://books.toscrape.com/catalogue/page-{i}.html", callback = self.parse)

    def parse(self, response):
        books = response.css('.product_pod')
        for book in books:
            a_url = book.css('h3 a::attr(href)').get()
            new_url = response.urljoin(a_url)
            yield response.follow(new_url, callback = self.parse_detail)

    def parse_detail(self, response):
        book_item =  BooksObtainItem()
        book_item['name'] = response.css('.active::text').get()
        book_item['price'] = float(response.css('.price_color ::text').get()[1::])
        book_item['subject'] = response.css('.breadcrumb li:nth-child(3) a::text').get()
        stock_str = response.xpath('//table[@class="table table-striped"]//tr[th[contains(., "Availability")]]/td/text()').get()
        book_item['stock'] = int(re.search(r'\((\d+)\s*available\)', stock_str).group(1))
        book_item['reviewers'] = int(response.xpath('//table[@class="table table-striped"]//tr[th[contains(., "Number of reviews")]]/td/text()').get())
        book_item['UPC'] = response.xpath('//table[contains(@class, "table-striped")]//tr[1]/td/text()').get()
        book_item['description'] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        rating_str = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[3]/@class').get()
        rating_dict = {   
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        book_item['rating'] = rating_dict[rating_str.split()[1]]
        img_src = response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').get()
        book_item['image'] = response.urljoin(img_src)
        print(book_item)
        return book_item