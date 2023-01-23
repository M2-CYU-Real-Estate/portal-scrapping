
from bs4 import BeautifulSoup as soup, BeautifulSoup, NavigableString, Tag  # HTML data structure
from urllib.request import urlopen as uReq, Request, urlopen  # Web client
import re
import json

class OuestFrance:

    filename = 'ouest.json'
    listCityCode = ["nice-06-06000", "marseille-13-13000","rennes-35-35000","paris-75-75000","nantes-44-44000",
                    "lyon-69-69000", "lille-59-59000", "poissy-78-78300", "cannes-06-06150", "toulouse-31-31000"]
    listIndexPage = [16, 14, 45, 4,10,140,2,1,3,16]


    def cleanData(self,data):
        x = re.sub("\s+", '', data)
        y = re.sub("[\xa0€m²-]", '', x)
        return y

    def writeData(self,list_of_dicts, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("[\n")
            for dic in list_of_dicts:
                for ligne in dic:
                    data = json.dumps(ligne, ensure_ascii=False)
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
            titre = container.find("span", {"class": "annTitre"})
            date = container.find("span", {"class": "annDebAff"})
            ville = container.find("span", {"class": "annVille"})

            if titre != None and ville !=None:
                titre = titre.text.split()
                titre = " ".join(titre)
                date = self.cleanData(date.text)
                ville = self.cleanData(ville.text)
                detailAnn = page_soup.findAll('a', class_='annLink')[index]
                ann = detailAnn.get('href')
                site = "https://www.ouestfrance-immo.com" + ann
                page_soup2 = self.downloaPage(site)
                listInfo = page_soup2.find("ul", {"class": "colGAnn"})
                desc = page_soup2.find("div", {"class": "txtAnn"})
                if desc != None:
                    desc = desc.text
                dictinfo = {}
                if listInfo != None:
                    for info in listInfo:
                        if isinstance(info, NavigableString):
                            continue
                        if isinstance(info, Tag):
                            if info.span != None and info.strong != None:
                                key = info.span.text
                                body = self.cleanData(info.strong.text)
                                dictinfo[key] = body
                else:
                    pass
                img = page_soup2.find('img', {"class": "lazy imgSlider"})
                if img != None:
                    img = img.get('data-original')
                ref = page_soup2.find('span', {"class": "ref"})
                if ref != None:
                    ref = self.cleanData(ref.text)
                if 'Prix' in dictinfo and 'Surf. habitable' in dictinfo and 'Pièces' in dictinfo:
                    annonces = {'ref': ref, 'url':site, 'title': titre, 'prix': dictinfo['Prix'],
                                'surface': dictinfo['Surf. habitable'], 'piece': dictinfo['Pièces'],
                                'ville': codePostale[0], 'codePostale': codePostale[2], 'annee': date, 'img': img,
                                'description': desc}
                    listAnnonces.append(annonces)
                else:
                    pass
            print('scrapped annonce', str(index))
        return  listAnnonces

    def main(self):
        listData = []
        for key, cityCode in enumerate(self.listCityCode):
            for index in range(self.listIndexPage[key]):
                listAnnonces = self.scrapOuestAnnonces(cityCode,index)
                listData.append(listAnnonces)

            self.writeData(listData, self.filename)

if __name__ == '__main__':
    OuestFrance().main()

