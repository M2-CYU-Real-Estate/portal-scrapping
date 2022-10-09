import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id', 'title', 'prix','prixm2','typeVente','ville','codePostale','img','description', 'surface', 'piece','etage', 'charge','annee']

class Door(CrawlSpider):
    name = 'door'
    allowed_domains = ['www.doorinsider.com']

    start_urls = [
        'https://www.doorinsider.com/fr/annonces-immobilieres/vente/france?page=1'
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
    def parse_item(self, response):
        try:
           self.title = response.css('h1.page-title::text').get()
           self.typeVente = response.xpath('.//div[@class="field field--name-field-type-property field--type-entity-reference field--label-visually_hidden"]/div/text()').getall()
           self.typeVente = self.typeVente[1]
           adresse = response.xpath('.//div[@class="field field--name-field-property-address field--type-address field--label-visually_hidden"]/div/text()').getall()
           adr = adresse[1].split()
           self.ville = adr[0]
           self.codePostale = adr[1]
           self.img = response.xpath('.//a[@class="photoswipe"]/@href')[0].get()
           self.surface = response.xpath('.//div[@class="field field--name-field-surface field--type-float field--label-inline clearfix"]/div/span/text()').get()
           self.surface = self.surface + " " + "m²"
           self.piece = response.xpath('.//div[@class="field field--name-field-number-of-rooms field--type-integer field--label-inline clearfix"]/div/text()')[1].get()
           self.etage = response.xpath('.//div[@class="field field--name-field-floor field--type-integer field--label-inline clearfix"]/div/text()')[1].get()
           self.annee = response.xpath('.//div[@class="field field--name-field-date-of-contruction field--type-integer field--label-inline clearfix"]/div/text()')[1].get()
           self.charge = response.xpath('.//div[@class="field field--name-extra-field-tax field--type-extra-field field--label-hidden field__items"]/div/text()').get()
           self.description = response.xpath('.//div[@class="field field--name-field-description field--type-string-long field--label-visually_hidden"]/div/text()')[1].get()
           self.prix = response.xpath('.//div[@class="field field--name-extra-field-display-price field--type-extra-field field--label-hidden field__items"]/div/text()').get()
           getPrixm2 = response.xpath('.//div[@class="field field--name-extra-field-price-per-square-meter field--type-extra-field field--label-hidden field__items"]/div/text()').get()
           getPrixm2 = getPrixm2.split()
           self.prixm2 = getPrixm2[1] + ''+ getPrixm2[2]
           print(self.prix)
        except:
            print("error: ", self.index)
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