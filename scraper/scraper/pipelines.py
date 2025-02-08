# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import csv

class SpotifyPipeline:
    
    def __init__(self):
        self.items = []
        
    def open_spider(self, spider):
        if spider.name == "artists":
            self.file = open('../output/artists_results.csv', 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Artist', 'Total_Streams', 'As_Lead', 'Solo', 'As_Feature', 'Daily_Streams', 'Daily_As_Lead', 'Daily_As_Feature', 'Tracks', 'Tracks_As_Lead', 'Tracks_Solo', 'Tracks_As_Feature'])   
                 
        elif spider.name == "countries":
            self.file = open('../output/countries_results.csv', 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Country', 'Pos', 'Artist_and_Title', 'Streams', 'Total'])
             
        elif spider.name == "listeners":
            self.file = open('../output/listeners_results.csv', 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Artist', 'Listeners', 'Peak', 'Peak_Listeners']) 
        
        elif spider.name == "toplists":
            self.file = open('../output/toplists_results.csv', 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Category', 'Position', 'Artist_and_Title', 'Streams', 'Daily'])
        else:    
            pass  

    def process_item(self, item, spider):
        def convert_to_int(value):
            """ Convertit une valeur en entier après suppression des virgules. """
            try:
                return int(value.replace(",", "")) if value else 0
            except ValueError:
                logging.warning(f"Impossible de convertir {value} en entier.")
                return 0

        def format_large_number(value):
            """ Formate un nombre entier avec des espaces pour améliorer la lisibilité. """
            return "{:,}".format(value).replace(",", " ")  

        if spider.name == "artists":
            if all(item.get(field) is not None for field in ['Artist', 'Total_Streams', 'As_Lead', 'Solo', 'As_Feature', 'Daily_Streams', 'Daily_As_Lead', 'Daily_As_Feature', 'Tracks', 'Tracks_As_Lead', 'Tracks_Solo', 'Tracks_As_Feature']):
                self.writer.writerow([
                    item.get('Artist'),
                    format_large_number(convert_to_int(item.get('Total_Streams'))),
                    format_large_number(convert_to_int(item.get('As_Lead'))),
                    format_large_number(convert_to_int(item.get('Solo'))),
                    format_large_number(convert_to_int(item.get('As_Feature'))),
                    format_large_number(convert_to_int(item.get('Daily_Streams'))),
                    format_large_number(convert_to_int(item.get('Daily_As_Lead'))),
                    format_large_number(convert_to_int(item.get('Daily_As_Feature'))),
                    format_large_number(convert_to_int(item.get('Tracks'))),
                    format_large_number(convert_to_int(item.get('Tracks_As_Lead'))),
                    format_large_number(convert_to_int(item.get('Tracks_Solo'))),
                    format_large_number(convert_to_int(item.get('Tracks_As_Feature')))
                ])
                logging.debug(f"Item ajouté : {item}")
            else:
                logging.debug(f"Item ignoré : {item} (valeurs manquantes)")

        elif spider.name == 'countries':
            if all(item.get(field) is not None for field in ['Country', 'Pos', 'Artist_and_Title', 'Streams', 'Total']):
                self.writer.writerow([
                    item.get('Country'),
                    convert_to_int(item.get('Pos')),
                    item.get('Artist_and_Title'),
                    format_large_number(convert_to_int(item.get('Streams'))),
                    format_large_number(convert_to_int(item.get('Total')))
                ])
                logging.debug(f"Item ajouté : {item}")
            else:
                logging.debug(f"Item ignoré : {item} (valeurs manquantes)")
            
        elif spider.name == 'listeners':
            if all(item.get(field) is not None for field in ['Artist', 'Listeners', 'Peak', 'Peak_Listeners']):
                self.writer.writerow([
                    item.get('Artist'),
                    convert_to_int(item.get('Listeners')),
                    convert_to_int(item.get('Peak')),
                    convert_to_int(item.get('Peak_Listeners'))
                ])
                logging.debug(f"Item ajouté : {item}")
            else:
                logging.debug(f"Item ignoré : {item} (valeurs manquantes)")

        elif spider.name == 'toplists':
            if all(item.get(field) is not None for field in ['Category', 'Position', 'Artist_and_Title', 'Streams', 'Daily']):
                self.writer.writerow([item.get('Category'), item.get('Position'), item.get('Artist_and_Title'), item.get('Streams'), item.get('Daily')])
                logging.debug(f"Item ajouté : {item}")
            else:
                logging.debug(f"Item ignoré : {item} (valeurs manquantes)")

        return item

    def close_spider(self, spider):
        self.file.close()
