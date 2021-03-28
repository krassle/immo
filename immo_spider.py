import scrapy

class QuotesSpider(scrapy.Spider):
    name = "immoscout"
    start_urls = [
            #'https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Fahrzeitsuche/Stuttgart/70569/-64516/2093406/-/-/45/2,00-/-/EURO--850,00'
            'https://www.immobilienscout24.de/Suche/de/bayern/fuerstenfeldbruck-kreis/germering/wohnung-mieten?haspromotion=false&numberofrooms=1.5-&price=-760.0&livingspace=30.0-&sorting=2',
            'https://www.immobilienscout24.de/Suche/de/bayern/muenchen/wohnung-mieten?haspromotion=false&numberofrooms=1.5-&price=-835.0&livingspace=30.0-&geocodes=1276002059095,1276002059027,1276002059107,1276002059108,1276002059111,1276002059113&sorting=2'
            ]
    def parse(self, response):
        for quote in response.css('a.result-list-entry__brand-title-container::attr(href)').extract():
            yield {
                "href": quote
                    }

