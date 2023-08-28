from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from Con_treinamentos.spiders.conTreinamentos import ContreinamentosSpider
from Con_treinamentos.spiders.conTreinamentosUrls import ContreinamentosUrlsSpider


def main():
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    runner.crawl(ContreinamentosSpider)
    runner.crawl(ContreinamentosUrlsSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    # the script will block here until all crawling jobs are finished
    reactor.run()

if __name__ == '__main__':
    main()