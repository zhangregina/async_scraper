from parsel import Selector
import asyncio
import httpx
from config import DEFAULT_HEADERS
from mongo_db.mongo_database import Mongo_DB


class DoramaScraper:
    ORIGINAL_URL = "https://doramy.club/serialy"
    MAIN_URL = "https://doramy.club/serialy/page/{}"
    SERIAL_URL = '//div[@class="post-home"]/a/@href'
    TITLE = '//h1[@itemprop="name"]/text()'
    SERIES = '//tbody[@class="tbody-sin"]//tr[2]/td[2]/text()'
    COUNTRY = '//tr[.//td[text()="Страна:"]]/td[2]/text()'
    YEAR = '//tr[.//td[text()="Год:"]]/td[2]/text()'
    GENRE = '//tr[.//td[text()="Жанр:"]]/td[2]/text()'
    IMAGE = '//div[@class="poster"]/img/@src'

    def __init__(self):
        self.all_pages = []
        self.all_urls = []
        self.mongo_database = Mongo_DB()

    async def get_all_pages(self):
        for i in range(1, 2):
            if i == 1:
                self.all_pages.append(self.ORIGINAL_URL)
            self.all_pages.append(self.MAIN_URL.format(i))
        for one_page in self.all_pages:
            content = httpx.get(one_page).text
            page_selector = Selector(text=content)
            self.all_urls.extend(page_selector.xpath(self.SERIAL_URL).extract())

    async def get_url(self, client, url):
        response = await client.get(url)
        await self.save_data(response.text)
        return response

    async def parse_data(self):
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS) as client:
            tasks = []
            for url in self.all_urls:
                tasks.append(asyncio.create_task(self.get_url(client, url)))
            serial_gather = await asyncio.gather(*tasks)
            await client.aclose()

    async def save_data(self, content):
        tree = Selector(text=content)
        url = tree.xpath(self.SERIAL_URL).get()
        title = tree.xpath(self.TITLE).extract_first()
        series = tree.xpath(self.SERIES).extract_first()
        country = tree.xpath(self.COUNTRY).extract_first()
        year = tree.xpath(self.YEAR).extract_first()
        genre = tree.xpath(self.GENRE).extract_first()
        image = tree.xpath(self.IMAGE).extract_first()

        serial_data = Mongo_DB.dorama_collection = {
            "current url": url,
            "title": title,
            "series": series,
            "country": country,
            "year": year,
            "genre": genre,
            "image": image,
            "date": Mongo_DB.dorama_collection.get("date"),
        }
        print(serial_data)
        await self.mongo_database.add_to_dorama_collection(dorama_objects=serial_data)

    async def main(self):
        await self.get_all_pages()
        await self.parse_data()


if __name__ == "__main__":
    scraper = DoramaScraper()
    asyncio.run(scraper.main())
