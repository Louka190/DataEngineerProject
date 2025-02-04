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
            link = row.css('td.text div a::attr(href)').get()
            if link:
                full_url = response.urljoin(link)
                yield scrapy.Request(url=full_url, callback=self.parse_song_page)

    def parse_song_page(self, response):
        """
        Analyse une page de détail pour extraire les informations spécifiques aux chansons.

        Args:
            response (scrapy.http.Response): La réponse de la requête vers la page de détail.

        Yields:
            SongDetailItem: Un item contenant les informations des chansons de la page.
        """
        rows = response.css('table.addpos.sortable tbody tr')

        for index, row in enumerate(rows, start=1):
            item = SongDetailItem()
            item['Position'] = index  # Position basée sur l'ordre des lignes
            item['Artist_and_Title'] = row.css('td.text div::text').get()
            item['Streams'] = row.css('td:nth-child(2)::text').get()
            item['Daily'] = row.css('td:nth-child(3)::text').get()

            if item['Artist_and_Title'] and item['Streams']:
                yield item
