import scrapy

class SBook(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    fecha_publicacion = scrapy.Field()
    idoma = scrapy.Field()
    ISBN = scrapy.Field()
    formato = scrapy.Field()
    presentacion = scrapy.Field()
    third_party_prices = scrapy.Field()

class SThirdPartyPrices(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
