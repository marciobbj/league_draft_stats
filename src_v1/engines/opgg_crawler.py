import scrapy

"""
Usage: open terminal and run:
    scrapy runspider .\engines\opgg_crawler.py -o .\storage\opgg\DATE_champion_tier_list.json
"""


class ChampionItem(scrapy.Item):
    rank = scrapy.Field()
    champion = scrapy.Field()
    tier = scrapy.Field()
    win_rate = scrapy.Field()
    pick_rate = scrapy.Field()
    ban_rate = scrapy.Field()
    weak_against = scrapy.Field()


class ChampionSpider(scrapy.Spider):
    name = "champion_spider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def __init__(self, region="br", tier="emerald_plus", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.positions = ["top", "mid", "jungle", "support", "adc"]
        self.region = region
        self.tier = tier
        self.start_urls = [
            f"https://www.op.gg/champions?region={self.region}&tier={tier}&position={position}"
            for position in self.positions
        ]

    def start_requests(self):
        headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        # Selecionando todas as linhas da tabela de campeões
        for row in response.xpath(
            '//table[contains(@class, "css-j5u3ca e1lge34e1")]/tbody/tr'
        ):
            item = ChampionItem()

            # Extraindo detalhes de cada linha
            item["rank"] = row.xpath(
                './/td[contains(@class, "css-ijscnw e1lge34e4")]/span[1]/text()'
            ).get()
            item["champion"] = row.xpath(
                './/td[contains(@class, "css-1im1udv e1lge34e2")]/a/strong/text()'
            ).get()
            item["tier"] = row.xpath(
                './/td[contains(@class, "css-1qn65js e1lge34e5")]/text()'
            ).get()
            item["win_rate"] = row.xpath(
                './/td[contains(@class, "css-9aydzo e1tupkk21")][1]/text()'
            ).get()
            item["pick_rate"] = row.xpath(
                './/td[contains(@class, "css-9aydzo e1tupkk21")][2]/text()'
            ).get()
            item["ban_rate"] = row.xpath(
                './/td[contains(@class, "css-9aydzo e1tupkk21")][3]/text()'
            ).get()

            # Para 'weak_against', como temos múltiplos elementos, precisamos iterar sobre eles
            weak_against = row.xpath(
                './/td[contains(@class, "css-6jlvp0 e1lge34e6")]/a/@href'
            ).getall()
            item["weak_against"] = [
                self.parse_weak_against_link(link) for link in weak_against
            ]

            yield item

    def parse_weak_against_link(self, link):
        if link:
            parts = link.split("&")
            for part in parts:
                if "target_champion=" in part:
                    return part.split("=")[-1]
        return None
