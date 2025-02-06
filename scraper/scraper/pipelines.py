# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#import pandas as pd
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
        if spider.name == "artists":
            self.writer.writerow([item.get('Artist'), item.get('Total_Streams'), item.get('As_Lead'), item.get('Solo'), item.get('As_Feature'), item.get('Daily_Streams'), item.get('Daily_As_Lead'), item.get('Daily_As_Feature'), item.get('Tracks'), item.get('Tracks_As_Lead'), item.get('Tracks_Solo'), item.get('Tracks_As_Feature')])
            logging.debug(f"Item ajouté : {item}")
            
        elif spider.name == 'countries':
            self.writer.writerow([item.get('Country'), item.get('Pos'), item.get('Artist_and_Title'), item.get('Streams'), item.get('Total')])
            logging.debug(f"Item ajouté : {item}")
            
        elif spider.name == 'listeners':
            self.writer.writerow([item.get('Artist'), item.get('Listeners'), item.get('Peak'), item.get('Peak_Listeners')])
            logging.debug(f"Item ajouté : {item}")

        elif spider.name == 'toplists':
            self.writer.writerow([item.get('Category'),item.get('Position'), item.get('Artist_and_Title'), item.get('Streams'), item.get('Daily')])
            logging.debug(f"Item ajouté : {item}")
        return item


    def close_spider(self, spider):
        self.file.close()
        #if spider.name == "artists":
        #    df = pd.read_csv('../output/artists_results.csv')
        #    df.dropna(inplace=True)
        #    df.to_csv('../output/artists_results_cleaned.csv', index=True)

