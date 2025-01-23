import scrapy
from ..items import ArticletItem


class OlympicsSpider(scrapy.Spider):
    """
    Un Spider Scrapy pour extraire des données sur les résultats olympiques 
    depuis le site olympedia.org.
    """
    name = "olympics"

    # Domaine autorisé pour éviter de scraper des sites non spécifiés
    allowed_domains = ["olympedia.org"]

    # URL de départ pour le scraping
    start_urls = ["https://www.olympedia.org/results/19000014"]

    def parse(self, response):
        """
        Méthode principale pour traiter la réponse de la page web.
        Cette méthode extrait les données du tableau et génère des éléments.

        :param response: L'objet réponse de Scrapy contenant le contenu de la page web.
        """
        # Extraction des en-têtes du tableau
        #headers = response.css('table.table-striped thead th::text').getall()
        #self.log(f"Headers extraits: {headers}")

        # Vérifier si le tableau contient un élément <tbody>
        tbody = response.css('table.table-striped tr')
        if not tbody:
            self.log("Le <tbody> n'a pas été trouvé.")
            return  

        # Sélecteur pour les lignes du tableau
        rows = tbody.css('tr')

        # Parcourir chaque ligne pour extraire les données
        for row in rows:
            # Créer un objet ArticletItem pour stocker les données de la ligne
            item = ArticletItem()

            # Extraction des données de chaque colonne du tableau
            item['Pos'] = row.css('td:nth-of-type(1)::text').get(default="N/A").strip()
            item['Swimmer'] = row.css('td:nth-of-type(2) a::text').get(default="N/A").strip()
            item['NOC'] = row.css('td:nth-of-type(3) a::text').get(default="N/A").strip()
            item['R1'] = row.css('td:nth-of-type(4)::text').get(default="N/A").strip()
            item['SF'] = row.css('td:nth-of-type(5)::text').get(default="N/A").strip()
            item['Final'] = row.css('td:nth-of-type(6)::text').get(default="N/A").strip()
            item['Medal'] = row.css('td:nth-of-type(7) span::text').get(default="N/A").strip()

            # Générer un élément pour le pipeline
            yield item
            self.log(f"Item généré: {item}")
