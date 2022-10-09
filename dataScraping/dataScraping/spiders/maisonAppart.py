import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id', 'title', 'prix','prixm2','typeVente','ville','codePostale','img','description', 'surface', 'piece','etage', 'charge', 'annee']

class Door(CrawlSpider):
    name = 'maison'
    allowed_domains = ['www.maisonsetappartements.fr']

    start_urls = [
        'https://www.maisonsetappartements.fr/fr/75/appartements/vente/selection-biens-paris-75000.html?page=1'
    ]

    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
        restrict_xpaths=('.//a[@class="pagi_passif"]')
    ),
        follow=True,
    )

    # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_extract = Rule(LinkExtractor(allow='https://www.maisonsetappartements.fr/fr/75/annonce-vente-appartement-paris',unique=True),
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
    charge = ""
    description=""
    autrePiece= ""
    def parse_item(self, response):
        try:
           getTitle = response.xpath(
                './/h2[@class="subtitle-ann"]/text()').get()
           self.title = getTitle
           self.prix = response.xpath(
               './/span[@class="prix-ann d-md-inline d-none float-md-right"]/text()').get()

           self.piece = response.xpath(
               './/div[@class="bandeau-bleu pt-2 pl-2 pl-lg-4"]/p/text()')[1].get()
           self.surface = response.xpath(
               './/div[@class="bandeau-bleu pt-2 pl-2 pl-lg-4"]/p/text()')[3].get()

           self.img = response.xpath('.//img[@class="w-100"]/@src').get()
           getVille = response.xpath(
               './/span[@class="d-block d-md-inline"]/text()')[1].get()
           codePostale = getVille.split()
           self.ville = codePostale[0] + " " + codePostale[1]
           self.codePostale = re.sub('[!@#$()]','',codePostale[2])
           self.description = response.xpath(
               './/div[@class="col-md-12 description-ann"]/p/text()').get()
          # print(codePostale)
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
                'charge': self.charge,
                'description': self.description
            }

            dataDic = {}
            dataDic.update(data)
            yield dataDic