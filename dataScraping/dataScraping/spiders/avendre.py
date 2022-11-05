import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import logging

DEBUG = False
FIELDS = [
    'id','ref', 'title', 'prix','prixm2','typeVente','ville','codePostale','img','accommodation','description', 'surface', 'piece','etage', 'charge', 'annee']


class Door(CrawlSpider):
    name = 'vendre'
    allowed_domains = ['www.avendrealouer.fr']

    start_urls = [
        'https://www.avendrealouer.fr/recherche.html?pageIndex=1&sortPropertyName=ReleaseDate&sortDirection=Descending&searchTypeID=1&type'
        'GroupCategoryID=1&localityIds=2-11,2-52,2-23,2-25,2-24,101-2310,2-53,2-94&typeGroupIds=1,2,10,11&hasAlert=unknow?page=1'
    ]

    # first get the next button which will visit every page of a category
    rule_next = Rule(LinkExtractor(
        restrict_xpaths=('.//a[@class="listing-item-link"]')
    ),
        follow=True,
    )

    # secondly # Extract links matching 'recipe' and parse them with the spider's method parse_item
    rule_extract = Rule(LinkExtractor(allow='/vente/',unique=True),
                       callback='parse_item',
                       follow=True)
    rules = (rule_extract, rule_next)

    index = 0
    ref = 0
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
    accommodation = ""
    def parse_item(self, response):
        try:
            getTitle = response.xpath(
                    './/div[@class="Criteria__DivStyledHead-sc-1ftsbop-0 gHTUJJ"]/h1/text()').get()
            self.title = getTitle
            if(self.title != None):
                getRef = response.xpath(
                    './/div[@class="Professional__DivStyledRef-sc-133x9p4-2 jGNyhI"]/text()').getall()
                self.ref = getRef[2]
                getTitle = getTitle.split()
                self.typeVente = getTitle[0]
                self.surface = response.xpath(
                    './/div[@class="CriteriaCriterion__DivStyledInformation-sc-16o7bzc-2 gORa-dQ"]/p/span/text()')[0].get()
                self.surface = re.sub('[^A-Za-z0-9]+', '', self.surface)
                self.surface = re.sub('[m]', '', self.surface)
                self.piece = response.xpath(
                    './/div[@class="CriteriaCriterion__DivStyledInformation-sc-16o7bzc-2 gORa-dQ"]/p/span/text()')[1].get()
                self.piece = re.sub('[^A-Za-z0-9]+', '', self.piece)
                self.annee = response.xpath(
                    './/div[@class="CriteriaCriterion__DivStyledInformation-sc-16o7bzc-2 gORa-dQ"]/p/span/text()')[3].get()
                getVille = response.xpath(
                    './/p[@class="Criteria__PStyledCity-sc-1ftsbop-7 leBNzy"]/text()').get()
                getVille = getVille.split("(")
                self.ville = getVille[0]
                self.codePostale = re.sub('[!@#$()]','',getVille[1])
                self.description = response.xpath(
                    './/p[@class="Professional__PStyled-sc-133x9p4-3 hQNjCq"]/text()').get()
                self.prix = response.xpath(
                    './/div[@class="Criteria__DivStyledValue-sc-1ftsbop-3 eZqQiC"]/text()').get()
                self.prix = re.sub('[^A-Za-z0-9]+', '', self.prix)
                self.prixm2 = response.xpath(
                    './/div[@class="Criteria__DivStyledPriceMetter-sc-1ftsbop-4 exjbmp"]/text()').get()
                self.prixm2 = re.sub('[^A-Za-z0-9]+', '', self.prixm2)

                self.img = response.xpath(
                    './/img[@class="SliderImages__ImgStyledSlider-sc-18z29ar-5 esrCRM adviewPhoto"]/@src').get()
                listAccommodation = response.xpath(
                    './/ul[@class="Professional__UlStyled-sc-133x9p4-6 gINLoU"]/li/text()').getall()
                dictAccomodation = {}
                if len(listAccommodation) >0:
                    for i in len(listAccommodation)+1:
                        dictAccomodation[listAccommodation[i+1]] = listAccommodation[i+2]
                    self.accommodation = dictAccomodation
                    print(self.accommodation)
        except:
            print("error: ", self.index)
        if self.title != None:
            self.index += 1
            data = {
                'id': self.index,
                'ref': self.ref,
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