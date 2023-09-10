import scrapy
from scrapy_playwright.page import PageMethod


class PaginationspiderSpider(scrapy.Spider):
    name = "paginationspider"
    page_number = 1

    def start_requests(self):
        yield scrapy.Request(
            "https://www.noon.com/egypt-en/p-17301/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                #    playwright_page_coroutines=[
                # This where we can implement scrolling if we want
                #       PageMethod("wait_for_selector", "img.sc-b51db3f-1.iCVkuj")
                #   ],
                errback=self.errback,
            ),
        )

    def parse(self, response):
        next_page = "https://www.noon.com/egypt-en/p-17301/?page=" + str(
            PaginationspiderSpider.page_number
        )
        if PaginationspiderSpider.page_number < 20:
            PaginationspiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse_links)

    def parse_links(self, response):
        tempLink = response.css("span.productContainer a::attr(href)").getall()
        link = "https://www.noon.com/egypt-en"
        for subLink in tempLink:
            yield response.follow(link + subLink, callback=self.parse_product_page)

    def parse_product_page(self, response):
        yield {
            "Name": response.css("h1::text").get(),
            # "description": response.xpath(
            #     "/html/body/div[1]/div/section/div/div[2]/div[1]/section/div/div/div[1]/div//text()"
            # ).getall(),
            # "category": response.xpath(
            #     response.xpath(
            #         "/html/body/div[1]/div/section/div/div[1]/div[1]/div/div/div/div/div/div/a//text()"
            #     ).get()
            # ).get(),
            "price": response.css("div.priceNow::text").getall(),
            # "image": response.xpath(
            #    "/html/body/div[1]/div/section/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div/div/div/div/div[1]/div/img//@src"
            # ).get(),
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
