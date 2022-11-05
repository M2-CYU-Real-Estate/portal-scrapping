
from bs4 import BeautifulSoup as soup, BeautifulSoup, NavigableString, Tag  # HTML data structure
from urllib.request import urlopen as uReq, Request, urlopen  # Web client
import re
import json

class OuestFrance:

    filename = 'ouest.json'
    #listCityCode = ["nice-06-06000", "marseille-13-13000","rennes-35-35000","paris-75-75000"]
    listCityCode = ["paris-75-75000"]
   # listIndexPage = [16, 4, 12]
    listIndexPage = [4]


    def cleanData(self,data):
        x = re.sub("\s+", '', data)
        y = re.sub("[\xa0€m²-]", '', x)
        return y

    def writeData(self,list_of_dicts, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("[\n")
            for dic in list_of_dicts:
                for ligne in dic:
                    data = json.dumps(ligne)
                    file.write(data)
                    file.write(",\n")
            file.write("]\n")
    def downloaPage(self,site):
        hdr = {'User-Agent': 'XYZ/3.0'}
        req = Request(site, headers=hdr)
        page = urlopen(req)
        page_soup = BeautifulSoup(page, "lxml")
        page.close()
        return page_soup

    def scrapOuestAnnonces(self,cityCode,indexPage):

        site = "https://www.ouestfrance-immo.com/acheter/" + cityCode + "/?types=207%2C201&" + "page=" + str(indexPage)
        codePostale = cityCode.split("-")
        page_soup = self.downloaPage(site)
        containers = page_soup.findAll("div", {"class": "annBlocDesc"})
        listAnnonces = []
        print('start scrapping....')
        for index, container in enumerate(containers):
            annonces = {}
            titre = container.find("span", {"class": "annTitre"})
            date = container.find("span", {"class": "annDebAff"})
            ville = container.find("span", {"class": "annVille"})

            if titre != None and ville !=None:
                titre = self.cleanData( titre.text)
                date =  self.cleanData(date.text)
                ville = self.cleanData(ville.text)
                detailAnn = page_soup.findAll('a', class_='annLink')[index]
                ann = detailAnn.get('href')
                site = "https://www.ouestfrance-immo.com" + ann
                page_soup2 = self.downloaPage(site)
                listInfo = page_soup2.find("ul", {"class": "colGAnn"})
                dictinfo = {}
                for info in listInfo:
                    if isinstance(info, NavigableString):
                        continue
                    if isinstance(info, Tag):
                        if info.span != None and info.strong != None:
                            key = info.span.text
                            body = self.cleanData(info.strong.text)
                            dictinfo[key] = body
                img = page_soup2.find('img', {"class": "lazy imgSlider"})
                if img != None:
                    img = img.get('data-original')
                ref = self.cleanData(page_soup2.find('span', {"class": "ref"}).text)
                annonces={'id': index,'ref':ref, 'date':date, 'titre': titre, 'ville': ville,'codePostale':codePostale[2],
                          'caracteristique': dictinfo, 'img':img}
                listAnnonces.append(annonces)
                print('scrapped annonce =>'+ str(index))

        return  listAnnonces

    def main(self):
        listData = []
        for key, cityCode in enumerate(self.listCityCode):
            for index in range(self.listIndexPage[key]):
                listAnnonces = self.scrapOuestAnnonces(cityCode,index)
                listData.append(listAnnonces)

        print(listData)
        self.writeData(listData, self.filename)

if __name__ == '__main__':
    OuestFrance().main()

