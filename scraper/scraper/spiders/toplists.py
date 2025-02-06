import scrapy
from ..items import SongItem

class TopListsSpider(scrapy.Spider):
    name = "toplists"
    allowed_domains = ["kworb.net"]
    start_urls = ["https://kworb.net/spotify/toplists.html"]

    def parse(self, response):
        """
        Analyse la page 'toplists.html' pour extraire la catégorie et le lien
        vers la page de détail. Ensuite, envoie une requête vers parse_song_link().
        """
        rows = response.xpath(
            "//span[contains(text(), 'Spotify most streamed songs')]/following::table[1]/tbody/tr"
        )

        for row in rows:
            category = row.xpath("./td[1]/text()").get()
            link = row.xpath("./td[2]/div/a/@href").get()
            link_text = row.xpath("./td[2]/div/a/text()").get()

            if category and category.strip():
                # On crée un item basique
                item = SongItem()
                item["Category"] = category.strip()
                item["Link_Text"] = link_text.strip() if link_text else None
                item["Relative_Link"] = link
                item["Absolute_Link"] = response.urljoin(link) if link else None

                if link:
                    # On envoie la requête vers la page du lien
                    yield scrapy.Request(
                        url=item["Absolute_Link"],
                        callback=self.parse_song_link,
                        meta={"base_item": item},
                    )
                else:
                    # Si pas de lien, on renvoie juste l'item
                    yield item

    def parse_song_link(self, response):
        """
        Récupère le SongItem de base, puis parcourt le tableau addpos sortable
        pour extraire Position, Artist_and_Title, Streams, et Daily.
        
        On veut un compteur différent par page, donc on le remet à 1 ici.
        """
        base_item = response.meta.get("base_item")
        
        rows = response.xpath("//table[contains(@class, 'addpos sortable')]/tbody/tr")

        # --- compteur local, redémarre à 1 pour chaque page ---
        position_counter = 1

        for row in rows:
            # Crée un item dérivé
            item = SongItem()

            # On recopie les champs de base
            item["Category"] = base_item["Category"]
            item["Link_Text"] = base_item["Link_Text"]
            item["Relative_Link"] = base_item["Relative_Link"]
            item["Absolute_Link"] = base_item["Absolute_Link"]

            # Position = compteur local
            item["Position"] = position_counter
            position_counter += 1

            # Extraction des autres colonnes
            artist_and_title = row.xpath("./td[1]/div/text()").get()
            streams = row.xpath("./td[2]/text()").get()
            daily = row.xpath("./td[3]/text()").get()

            item["Artist_and_Title"] = artist_and_title.strip() if artist_and_title else None
            item["Streams"] = streams.strip() if streams else None
            item["Daily"] = daily.strip() if daily else None

            yield item
