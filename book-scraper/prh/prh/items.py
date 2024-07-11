# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SBook(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    publication_date = scrapy.Field()
    imprint = scrapy.Field()
    third_party_prices = scrapy.Field()
    prh_details = scrapy.Field()

class SThirdPartyPrices(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()

class SPRHDetails(scrapy.Item):
    colleccion = scrapy.Field()
    paginas = scrapy.Field()
    target_de_edad = scrapy.Field()
    tipo_de_encuadernacion = scrapy.Field()
    idioma = scrapy.Field()
    fecha_de_publicacion = scrapy.Field()
    autor = scrapy.Field()
    editorial = scrapy.Field()
    referencia = scrapy.Field()