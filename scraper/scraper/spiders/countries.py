import scrapy
from ..items import CountryItem

class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/"]

    def parse(self, response):
        """
        Analyse la page principale pour extraire les noms des pays et leurs URLs associées.
        
        Args:
            response (scrapy.http.Response): La réponse de la requête initiale.
        
        Yields:
            scrapy.Request: Une requête vers la page du pays avec un callback vers parse_country.
        """
        rows = response.css('table tr')

        for row in rows:
            country_name = row.css('td.mp.text::text').get()

            if country_name and country_name.strip():  # Vérification si le nom n'est pas vide
                # Création de l'item pour le pays
                item = CountryItem()
                item['Country'] = country_name.strip()

                # Construction de l'URL pour la page du pays
                country_code = row.css('td.mp.text a::attr(href)').re_first(r'country/(\w+)_daily.html')
                if country_code:
                    country_url = f"https://kworb.net/spotify/country/{country_code}_weekly.html"
                    # Envoi de la requête vers la page du pays
                    yield scrapy.Request(
                        url=country_url,
                        callback=self.parse_country,
                        meta={'item': item}
                    )
    
    def parse_country(self, response):
        """
        Analyse la page d'un pays pour extraire les informations des chansons.
        
        Args:
            response (scrapy.http.Response): La réponse de la requête vers la page du pays.
        
        Yields:
            CountryItem: Un item contenant les informations des chansons pour un pays donné.
        """
        item = response.meta['item']
        
        rows = response.css('table#spotifyweekly tbody tr')

        for row in rows:
            item['Pos'] = row.css('td.np::text').get()
            item['Artist_and_Title'] = row.css('td.text.mp div a::text').getall()
            item['Streams'] = row.css('td:nth-child(7)::text').get()
            item['Total'] = row.css('td:nth-child(9)::text').get()

            yield item
