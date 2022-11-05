import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id', 'ref','title', 'prix','typeVente','ville','codePostale','img','description', 'surface', 'piece', 'annee']

class Door(CrawlSpider):
    name = 'maison'
    allowed_domains = ['www.maisonsetappartements.fr']

    start_urls = [
        'https://www.maisonsetappartements.fr/views/Search.php?lang=fr&departement=&villes=38344,2123,32549,24744,4775,4776,4777,4778,4779,4780,4781,4784,4785,4786,4787,4788,4789,4790,14823,13171,13742,17979,2006&nb_km=&TypeAnnonce=VEN&TypeBien=&bdgMin=&bdgMax=&surfMin=&surfMax=&nb_piece=&keywords=&quartier=21173&page=1'
    ]

    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
        restrict_xpaths=('.//a[@class="pagi_passif"]')
    ),
        follow=True,
    )

    # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_extract = Rule(LinkExtractor(allow='https://www.maisonsetappartements.fr/fr/',unique=True),
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
                './/h2[@class="subtitle-ann"]/text()').get()
           if getTitle !=None:
               ref = response.xpath(
                   './/span[@class="d-block d-md-inline mt-1 mt-md-0"]/text()')[-1].get()
               self.ref =  re.sub('\W+', '', ref)
               self.title = getTitle
               getTitle = getTitle.split(" ")
               self.typeVente = getTitle[0] + " " + getTitle[1]
               prix = response.xpath(
                   './/span[@class="prix-ann d-md-inline d-none float-md-right"]/text()').get()
               self.prix= re.sub('\W+', '', prix)
               self.piece = response.xpath(
                   './/div[@class="bandeau-bleu pt-2 pl-2 pl-lg-4"]/p/text()')[1].get()
               self.piece= re.sub('\W+', '', self.piece)
               self.piece= re.sub('[pièces]', '', self.piece)
               surface = response.xpath(
                   './/div[@class="bandeau-bleu pt-2 pl-2 pl-lg-4"]/p/text()')[3].get()
               self.surface= re.sub('\W+', '', surface)
               self.surface= re.sub('[m²]', '', self.surface)
               self.img = response.xpath('.//img[@class="w-100"]/@src').get()
               getVille = response.xpath(
                   './/span[@class="d-block d-md-inline"]/text()')[1].get()
               codePostale = getVille.split()
               self.ville = codePostale[0]
               self.codePostale = re.sub('[!@#$()]','',codePostale[1])
               self.description = response.xpath(
                   './/div[@class="col-md-12 description-ann"]/p/text()').get()
          # print(codePostale)
        except:
            print("error: ", self.index)
        if getTitle != None:
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