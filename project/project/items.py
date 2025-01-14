# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticletItem(scrapy.Item):
    
    """    
    Définition des champs de l'item pour Scrapy
    Représente les données extraites du tableau des nageurs de 100m freestyle du site Olympedia 
    Pos = Position du nageur
    Swimmer = Nom du nageur
    NOC = Nationalité du nageur
    R1 = Temps de la première course
    SF = Temps de la demi-finale
    Final = Temps de la finale
    Medal = Médaille gagnée
    """    
    
    Pos	= scrapy.Field()
    Swimmer = scrapy.Field()
    NOC	= scrapy.Field()
    R1 = scrapy.Field()
    SF = scrapy.Field()	
    Final = scrapy.Field()
    Medal = scrapy.Field()

