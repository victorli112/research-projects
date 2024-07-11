from bs4 import BeautifulSoup
import scrapy

from prh.items import SBook, SPRHDetails, SThirdPartyPrices
from prh.spiders.prh_helper import PRHHelper
from prh.spiders.third_party_helper import ThirdPartyHelper

# do the same as scrape_prh.py but with scrapy
class spiders(scrapy.Spider):
    name = "prh-scraper"
    handle_httpstatus_list = [404, 500]
    start_urls = ["https://www.penguinlibros.com/ar/40915-aventuras",
                 "https://www.penguinlibros.com/ar/40919-fantasia",
                 #"https://www.penguinlibros.com/ar/40925-literatura-contemporanea?pageno=50",]
                 "https://www.penguinlibros.com/ar/40929-novela-negra-misterio-y-thriller",
                 "https://www.penguinlibros.com/ar/40933-poesia",
                 "https://www.penguinlibros.com/ar/40917-ciencia-ficcion",
                 "https://www.penguinlibros.com/ar/40923-grandes-clasicos",
                 "https://www.penguinlibros.com/ar/40927-novela-historica",
                 "https://www.penguinlibros.com/ar/40931-novela-romantica"]
    
    
    RETRY_HTTP_CODES = [502, 503, 504, 522, 524, 408, 429, 400]
    custom_settings = {
        "RETRY_HTTP_CODES": [502, 503, 504, 522, 524, 408, 429, 400],
        "handle_httpstatus_list": [404, 500],
    }
    dont_parse_third_party = ["bajalibros", "play", "goto", "amazon", "audible"]
    links = set()
    tracking_third_party_links = set()
    num_duplicates = 0
    
    def parse(self, response):
        # we might still be getting a response from 500 errors
        if response.status == 500 or response.status == 404:
            print("//////////////////// 500 ERROR PARSE ///////////////////////////////", response.url)
           
        # Category of request separated by _
        category = '_'.join(response.request.url.split("/")[-1].split("-")[1:]).split('?')[0]
        if category == 'novela_negra_misterio_y_thriller':
            category = 'novela_misterio_y_thriller'
        
        # Get all books on the page
        all_books = response.css('p.productTitle a::attr(href)').getall()
        for book in all_books:
            
            # Keep track of duplicate books
            if (book, category) in self.links:
               self.num_duplicates += 1
               if self.num_duplicates % 100 == 0:
                   print(f"[COUNT] Processed {self.num_duplicates} duplicates.")
               continue
            else:
               self.links.add((book, category))
               
            yield scrapy.Request(book, callback=self.parse_book, meta={'category': category}, dont_filter=True)
        
        # Go to next page if it exists and there are books on this page
        if "pageno" in response.request.url:
            next_page = response.request.url.split("pageno=")[0] + "pageno=" + str(int(response.request.url.split("pageno=")[1]) + 1)
            #page = int(response.request.url.split("pageno=")[1]) + 1
        else:
            next_page = response.request.url + "?pageno=2"
            #page = 2
        if next_page and len(all_books) > 0:
            #batching
            #if page > 49:
            #    print(f'On page {page}')
            yield scrapy.Request(next_page, callback=self.parse)
            
    def parse_book(self, response):
        if response.status == 500 or response.status == 404:
            print(f"//////////////////// {response.status} ERROR PARSE BOOK /////////////////////////////// {response.url}")
            
        book_soup = BeautifulSoup(response.body, 'lxml')
    
        # Initialize helper class to store data
        helper = PRHHelper()
    
        # Get basic information
        try:
            helper.populate_prh_basic_info(book_soup)
            helper.populate_prh_detailed_info(book_soup)
        except:
            print("Can't parse prh info", response.url, response.status)
            if response.status in [404, 500]:
                print("Retrying request", response.request.url)
                yield scrapy.Request(response.request.url, 
                                     callback=self.parse_book, 
                                     dont_filter=True, 
                                     meta={'category': response.meta['category']})
                return
        
        # Populate scrapy item
        item = SBook(category=response.meta["category"],
                     title=helper.title, 
                     author=helper.author, 
                     price=helper.price, 
                     publication_date=helper.publication_date, 
                     imprint=helper.imprint, 
                     third_party_prices=[], 
                     prh_details=SPRHDetails(colleccion=helper.colleccion, 
                                             paginas=helper.paginas, 
                                             target_de_edad=helper.target_de_edad, 
                                             tipo_de_encuadernacion=helper.tipo_de_encuadernacion, 
                                             idioma=helper.idioma, 
                                             fecha_de_publicacion=helper.fecha_de_publicacion, 
                                             autor=helper.autor, 
                                             editorial=helper.editorial, 
                                             referencia=helper.referencia
                                             )
                     )
        
        # Iterate through all third party links
        for link in response.css('div.bloque_external_link a::attr(href)').getall():
            if any(x in link for x in self.dont_parse_third_party):
                continue
            if (link, response.meta['category'], helper.title, helper.author) in self.tracking_third_party_links:
                continue
            else:
                self.tracking_third_party_links.add((link, response.meta['category'], helper.title, helper.author))
                yield scrapy.Request(link, callback=self.parse_third_party, dont_filter=True, meta={'item': item, 'url': link, 'bookTitle':helper.title})
        
    def parse_third_party(self, response):
        price = ThirdPartyHelper()
        soup = BeautifulSoup(response.body, 'lxml')
        price.populate_price(soup, response.meta['url'], response.meta['bookTitle'])
        
        item = SThirdPartyPrices(name=price.name, price=price.price, discount=price.discount)
        book_item = response.meta['item']
        book_item['third_party_prices'].append(item)
        return book_item
        
