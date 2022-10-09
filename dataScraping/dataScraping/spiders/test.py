import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id', 'nom'
]

class Door(CrawlSpider):
    name = 'test'
    allowed_domains = ['www.doorinsider.com']

    start_urls = [
        'https://www.doorinsider.com/fr/annonces-immobilieres/vente/france?page=181'
    ]

    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
        restrict_xpaths=('.//nav[@class="pager"]/ul/li/a')
    ),
        follow=True,
    )

    # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_recipe = Rule(LinkExtractor(allow='/fr/annonces-immobilieres/vente/france/', unique=True),
                       callback='parse_item',
                       follow=True,
                       )
    rules = (rule_recipe, rule_next)

    def parse_item(self, response):
       try:
           page = response.url.split("/")[-2]
           filename = f'door-{page}.html'
           with open(filename, 'wb') as f:
               f.write(response.body)
       except:
            print("error")