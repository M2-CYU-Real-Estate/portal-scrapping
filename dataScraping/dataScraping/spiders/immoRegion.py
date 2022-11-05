import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id','ref', 'title', 'prix','typeVente','ville','codePostale','img','description', 'surface', 'piece','etage', 'annee']

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
    ref = 0
    prix = 0
    title = ""
    img=""
    typeVente = ""
    piece=""
    ville=""
    codePostale=""
    surface=""
    annee = ""
    description=""
    def parse_item(self, response):
        try:
            getTitle = response.xpath(
                './/h1[@class="KeyInfoBlockStyle__PdpTitle-sc-1o1h56e-2 ilPGib"]/text()').get()
            self.title = getTitle
            if getTitle != None:
                getTitle = getTitle.split()
                self.typeVente = getTitle[0]
                self.ref = response.xpath(
                    './/div[@class="DescriptionStyle__DescriptionMoreReferences-sc-dqxmgt-11 kMeszr"]/p/text()')[1].get()
                self.prix = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__Price-sc-1o1h56e-5 fpNLMn"]/h2/text()').get()
                self.prix= re.sub('\W+', '', self.prix)
                self.ville =getTitle[-1]
                self.piece = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__LogoContainer-sc-1o1h56e-11 FKviO"]/ul/li/div/span/text()')[0].get()
                self.piece= re.sub('\W+', '', self.piece)
                surface = response.xpath(
                    './/div[@class="KeyInfoBlockStyle__LogoContainer-sc-1o1h56e-11 FKviO"]/ul/li/div/span/text()')[
                    4].get()
                surface= surface.split(" ")
                self.surface = surface[0]
                self.img = response.xpath("//meta[@name='og:image']/@content")[0].extract()
                self.description = response.xpath(
                    './/div[@class="collapsed"]/p/text()').get()
                getAnnee = response.css('div.feature-bloc')
                self.annee = getAnnee[1].xpath('.//ul/li/div[@class="feature-bloc-content-specification-content-response"]/div/text()')[5].get()
        except:
            print("error: ", self.index)
        if self.title != None:
            self.index += 1
            data = {
                'id': self.index,
                'ref': self.ref,
                'title': self.title,
                'prix': self.prix,
                'typeVente': self.typeVente,
                'ville': self.ville,
                'codePostale': self.codePostale,
                'img': self.img,
                'surface': self.surface,
                'piece': self.piece,
                'annee': self.annee,
                'description': self.description
            }

            dataDic = {}
            dataDic.update(data)
            yield dataDic