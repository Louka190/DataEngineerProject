import scrapy
from ..items import CountryItem

class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/"]

    def parse(self, response):
        """
        Méthode principale pour traiter la réponse de la page web.
        Cette méthode extrait les noms des pays du tableau.
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
        Méthode pour traiter la réponse de la page web d'un pays.
        Cette méthode extrait les détails des artistes et des titres.
        """
        item = response.meta['item']
        
        rows = response.css('table#spotifyweekly tbody tr')

        for row in rows:
            item['Pos'] = row.css('td.np::text').get()
            item['Artist_and_Title'] = row.css('td.text.mp div a::text').getall()
            item['Streams'] = row.css('td:nth-child(7)::text').get()
            item['Total'] = row.css('td:nth-child(9)::text').get()

            yield item
