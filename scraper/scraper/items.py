# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpotifyItem(scrapy.Item):
    Artist = scrapy.Field()
    Total_Streams = scrapy.Field()
    As_Lead = scrapy.Field()
    Solo = scrapy.Field()
    As_Feature = scrapy.Field()
    Daily_Streams = scrapy.Field()
    Daily_As_Lead = scrapy.Field()
    Daily_Solo = scrapy.Field()
    Daily_As_Feature = scrapy.Field()
    Tracks = scrapy.Field()
    Tracks_As_Lead = scrapy.Field()
    Tracks_Solo = scrapy.Field()
    Tracks_As_Feature = scrapy.Field()

class CountryItem(scrapy.Item):
    Country = scrapy.Field()
    Pos = scrapy.Field()
    Artist_and_Title = scrapy.Field()
    Streams = scrapy.Field()
    Total = scrapy.Field()

class ListenerItem(scrapy.Item):
    Artist = scrapy.Field()
    Listeners = scrapy.Field()
    #Daily_Trend = scrapy.Field()
    Peak = scrapy.Field()
    Peak_Listeners = scrapy.Field()