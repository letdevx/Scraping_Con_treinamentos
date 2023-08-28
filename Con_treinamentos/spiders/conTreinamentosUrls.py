from datetime import datetime
import scrapy

class ContreinamentosUrlsSpider(scrapy.Spider):
    name = "conTreinamentosUrls"
    start_urls = ["https://contreinamentos.com.br/cursos/"]
    time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    custom_settings = {
        'FEEDS': {
            f'results/contreinamentosUrls_{time}.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        """Coleta as urls dos cursos e eventos."""
        urls_cursos = response.xpath(
            '//div[contains(@class, "elementor-button-wrapper")]/a/@href').extract()
        urls_eventos = response.xpath('//*[@id="content"]//div[@class="elementor-flip-box"]//a/@href').extract()

        for url in urls_cursos + urls_eventos:
            
            yield{
                'url-curso' : url
            }