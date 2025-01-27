import scrapy
from ..items import SpotifyItem


class ArtistsSpider(scrapy.Spider):
    
    name = "artists"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/artists.html"]

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

        # Parcourir chaque ligne pour extraire les liens vers les pages des artistes
        for row in rows:
            # Extraction du lien relatif de l'artiste
            artist_url = row.css('td.text a::attr(href)').get()

            if artist_url:
                # Compléter l'URL en ajoutant le domaine de base
                artist_url = response.urljoin(artist_url)

                # Faire une requête vers la page de l'artiste
                yield scrapy.Request(artist_url, callback=self.parse_artist)

            # Extraire aussi les autres informations du tableau
            #item = SpotifyItem()
            #item['Artist'] = row.css('td.text a::text').get()
            
            #yield item

    def parse_artist(self, response):
        item = SpotifyItem()
        item['Artist'] = response.css('span.pagetitle::text').get().split(' - ')[0]
        item['Total_Streams'] = response.css('tr:contains("Streams") td:nth-child(2)::text').get()
        item['As_Lead'] = response.css('tr:contains("Streams") td:nth-child(3)::text').get()
        item['Solo'] = response.css('tr:contains("Streams") td:nth-child(4)::text').get()
        item['As_Feature'] = response.css('tr:contains("Streams") td:nth-child(5)::text').get()
        item['Daily_Streams'] = response.css('tr:contains("Daily") td:nth-child(2)::text').get()
        item['Daily_As_Lead'] = response.css('tr:contains("Daily") td:nth-child(3)::text').get()
        item['Daily_Solo'] = response.css('tr:contains("Daily") td:nth-child(4)::text').get()
        item['Daily_As_Feature'] = response.css('tr:contains("Daily") td:nth-child(5)::text').get()
        item['Tracks'] = response.css('tr:contains("Tracks") td:nth-child(2)::text').get()
        item['Tracks_As_Lead'] = response.css('tr:contains("Tracks") td:nth-child(3)::text').get()
        item['Tracks_Solo'] = response.css('tr:contains("Tracks") td:nth-child(4)::text').get()
        item['Tracks_As_Feature'] = response.css('tr:contains("Tracks") td:nth-child(5)::text').get()
        yield item
