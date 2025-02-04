import scrapy
from ..items import SongDetailItem

class TopListsSpider(scrapy.Spider):
    name = "toplists"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/toplists.html"]

    def parse(self, response):
        """
        Analyse la page principale pour extraire les liens vers les pages de détail.

        Args:
            response (scrapy.http.Response): La réponse de la requête initiale.

        Yields:
            scrapy.Request: Une requête vers la page de détail avec un callback vers parse_song_page.
        """
        rows = response.css('table tbody tr')

        for row in rows:
            # Récupérer le titre et l'URL
            song_title = row.css('td.text div a::text').get()
            relative_link = row.css('td.text div a::attr(href)').get()

            if song_title and relative_link:
                # Création de l'item avec le titre
                item = SongDetailItem()
                item['Artist_and_Title'] = song_title.strip()

                # Construire l'URL complète
                full_url = response.urljoin(relative_link)

                # Envoi de la requête vers la page de détail
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_song_page,
                    meta={'item': item}
                )

    def parse_song_page(self, response):
        """
        Analyse une page de détail pour extraire les informations spécifiques aux chansons.

        Args:
            response (scrapy.http.Response): La réponse de la requête vers la page de détail.

        Yields:
            SongDetailItem: Un item contenant les informations des chansons de la page.
        """
        item = response.meta['item']

        # Extraire les informations de chaque ligne du tableau
        rows = response.css('table.addpos.sortable tbody tr')

        for row in rows:
            # Ajouter les champs manquants à l'item
            item['Position'] = row.css('td:nth-child(1)::text').get()
            item['Streams'] = row.css('td:nth-child(2)::text').get()
            item['Daily'] = row.css('td:nth-child(3)::text').get()

            yield item
