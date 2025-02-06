# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpotifyItem(scrapy.Item):
    """
    Item pour stocker les informations de streaming d'un artiste.
    """
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
    """
    Item pour stocker les informations des chansons d'un pays.
    """
    Country = scrapy.Field()
    Pos = scrapy.Field()
    Artist_and_Title = scrapy.Field()
    Streams = scrapy.Field()
    Total = scrapy.Field()

class ListenerItem(scrapy.Item):
    """
    Item pour stocker les informations des auditeurs d'un artiste.
    """
    Artist = scrapy.Field()
    Listeners = scrapy.Field()
    #Daily_Trend = scrapy.Field()
    Peak = scrapy.Field()
    Peak_Listeners = scrapy.Field()

class SongItem(scrapy.Item):
    Category = scrapy.Field()
    Link_Text = scrapy.Field()
    Relative_Link = scrapy.Field()
    Absolute_Link = scrapy.Field()

    Position = scrapy.Field()
    Artist_and_Title = scrapy.Field()
    Streams = scrapy.Field()
    Daily = scrapy.Field()
