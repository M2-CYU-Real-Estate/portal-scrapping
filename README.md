# portal-scrapping
The classes are under le spiders folder. For each site that we scrape we created a file.
~~~
/dataScraping/dataScrapin/spiders
~~~
To run the project you need to enter in terminal:

~~~
 scrapy crawl sracpy_name 
~~~~

To run the project and generate a json file :

~~~~
 scrapy crawl scrapy_name -o file.json
~~~~

The scrapy_name can be found under le class with the variable: name

# Scraped data
We have 14371 rows of data for testing purpose.

# Data structure
<strong>ref: </strong> reference de l'annonce. <br>
<strong>title: </strong> titre  de l'annonce.  <br>
<strong>prix: </strong> prix de l'annonce.  <br>
<strong>surface: </strong> surface du bien.  <br>
<strong>piece: </strong> nombre de pièce  de l'annonce.  <br>
<strong>ville: </strong> la ville du bien.  <br>
<strong>codePostale: </strong> code postale  de l'annonce.  <br>
<strong>annee: </strong> anne de construction du bien.  <br>
<strong>description: </strong>description du bien.  <br>
<strong>typeVente: </strong> type de bien (maison / appart...).  <br>
<strong>img: </strong> l'image du bien.

