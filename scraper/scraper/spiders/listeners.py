import scrapy
from ..items import ListenerItem

class ListenersSpider(scrapy.Spider):
    
    name = "listeners"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/listeners.html"]

    def parse(self, response):
        """
        Méthode principale pour traiter la réponse de la page web.
        Cette méthode extrait les données du tableau et génère des liens vers les pages des artistes.

        :param response: L'objet réponse de Scrapy contenant le contenu de la page web.
        """
        # Extraction des lignes du tableau
        tbody = response.css('table.addpos tbody tr')
        if not tbody:
            self.log("Le <tbody> n'a pas été trouvé.")
            return

        # Sélecteur pour les lignes du tableau
        rows = tbody.css('tr')

        # Parcourir chaque ligne pour extraire les données
        for row in rows:

            # Extraire aussi les autres informations du tableau
            item = ListenerItem()
            item['Artist'] = row.css('td.text a::text').get()
            item['Listeners'] = row.css('td:nth-child(2)::text').get()
            #item['Daily_Trend'] = row.css('td:nth-child(3)::text').get()
            item['Peak'] = row.css('td:nth-child(4)::text').get()
            item['Peak_Listeners'] = row.css('td:nth-child(5)::text').get()
            
            yield item
