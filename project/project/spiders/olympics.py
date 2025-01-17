import scrapy
import json
from ..items import ArticletItem


class OlympicsSpider(scrapy.Spider):
    name = "olympics"

    # Domaine
    allowed_domains = ["olympedia.org"]

    # URL de la page à scraper
    start_urls = ["https://www.olympedia.org/results/19000014"]

    def parse(self, response):
        """
        Scraper les données du tableau et les enregistrer dans un fichier JSON.
        """

        headers = response.css('table.table-striped thead th::text').getall()[0:7]

        # Vérifier si le <tbody> existe dans la page
        tbody = response.css('table.table-striped tr')
        if not tbody:
            self.log("Le <tbody> n'a pas été trouvé.")
            return  

        # Sélecteur pour les lignes du tableau dans le <tbody>
        rows = tbody.css('tr')

        # Liste pour stocker les données extraites
        table_data = []

        for row in rows:

            item = ArticletItem()

            # Extraction des données de chaque colonne
            item['Pos'] = row.css('td:nth-of-type(1)::text').get(default="N/A").strip()
            item['Swimmer'] = row.css('td:nth-of-type(2) a::text').get(default="N/A").strip()
            item['NOC'] = row.css('td:nth-of-type(3) a::text').get(default="N/A").strip()
            item['R1'] = row.css('td:nth-of-type(4)::text').get(default="N/A").strip()
            item['SF'] = row.css('td:nth-of-type(5)::text').get(default="N/A").strip()
            item['Final'] = row.css('td:nth-of-type(6)::text').get(default="N/A").strip()
            item['Medal'] = row.css('td:nth-of-type(7) span::text').get(default="N/A").strip()

            table_data.append(dict(item))

        table_data = table_data[1:71]

        # Créer une structure JSON avec les en-têtes et les lignes de données
        results = {
            "Headers": headers,
            "Data": table_data
        }

        # Sauvegarder les données dans un fichier JSON avec un encodage UTF-8
        output_file = "olympics_results.json"
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

        self.log(f"Les données ont été enregistrées dans '{output_file}'.")
