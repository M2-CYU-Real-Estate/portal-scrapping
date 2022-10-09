import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id', 'title', 'prix','prixm2','typeVente','ville','codePostale','img','description', 'surface', 'piece','etage', 'annee']

class Door(CrawlSpider):
    name = 'immo'
    allowed_domains = ['www.immoregion.fr']

    start_urls = [
        'https://www.immoregion.fr/vente/maison?page=1'
    ]

    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
        restrict_xpaths=('.//a[@class="page"]')
    ),
        follow=True,
    )

    # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_extract = Rule(LinkExtractor(allow=r'/id-',unique=True),
                       callback='parse_item',
                       follow=True)
    rules = (rule_extract, rule_next)

    index = 0
    prix = 0
    prixm2 = 0
    title = ""
    img=""
    typeVente = ""
    piece=""
    ville=""
    codePostale=""
    surface=""
    etage = ""
    annee = ""
    description=""
    autrePiece= ""
    def parse_item(self, response):
        try:
            getTitle = response.xpath(
                './/h1[@class="KeyInfoBlockStyle__PdpTitle-sc-1o1h56e-2 hWEtva"]/text()').get()
            self.title = getTitle
            if getTitle != None:
                getTitle = getTitle.split()
                self.typeVente = getTitle[0]
                self.prix = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__Price-sc-1o1h56e-5 eWOlhG"]/h2/text()').get()
                self.prix = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__Price-sc-1o1h56e-5 eWOlhG"]/h2/text()').get()
                self.ville =getTitle[-1]
                self.piece = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__LogoContainer-sc-1o1h56e-11 FKviO"]/ul/li/div/span/text()')[0].get()
                self.surface = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__LogoContainer-sc-1o1h56e-11 FKviO"]/ul/li/div/span/text()')[
                    4].get()
                self.img = response.xpath("//meta[@name='og:image']/@content")[0].extract()
                self.description = response.xpath(
                    './/div[@class="collapsed"]/p/text()').get()
                getAnnee = response.css('div.feature-bloc')
                self.annee = getAnnee[1].xpath('.//ul/li/div[@class="feature-bloc-content-specification-content-response"]/div/text()')[5].get()
                print(self.annee)
        except:
            print("error: ", self.index)
        if self.title != None:
            self.index += 1
            data = {
                'id': self.index,
                'title': self.title,
                'prix': self.prix,
                'prixm2': self.prixm2,
                'typeVente': self.typeVente,
                'ville': self.ville,
                'codePostale': self.codePostale,
                'img': self.img,
                'surface': self.surface,
                'piece': self.piece,
                'etage': self.etage,
                'annee': self.annee,
                'description': self.description
            }

            dataDic = {}
            dataDic.update(data)
            yield dataDic