# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from xlsxwriter import Workbook

from planeta.items import SBook

THIRD_PARTY_PLANETA = ['Tematika', 'Cuspide', 'SBS_Liberia', 'Tras_los_Pasos', 'Libros_de_la_Arena', 'Libreria_Palito', 'Libreria_Santa_Fe']
class ExcelWriterPipeline:
    def open_spider(self, spider):
        self.row = 1
        self.results = {
            'novela_contemporanea': {},
            'novela_historica': {},
            'novela_literaria': {},
            'novela_negra': {},
            'novelas_romanticas': {},
            'poesia': {},
            'teatro': {}
        }
        self.num_books = 0
        
    def close_spider(self, spider):
        # TO EXCEL 
        print(f"FINAL Processed {self.num_books} books, counts of each category: {[(k, len(v)) for k, v in self.results.items()]}")
        
        ordered_columns = ['Title', 'Author', 'Price', 'Fecha Publicacion', 'Idoma', 'ISBN', 'Formato', 'Presentacion', 'price_in_Tematika', 'discount_Tematika', 'price_in_Cuspide', 'discount_Cuspide', 'price_in_SBS_Liberia', 'discount_SBS_Liberia', 'price_in_Tras_los_Pasos', 'discount_Tras_los_Pasos', 'price_in_Libros_de_la_Arena', 'discount_Libros_de_la_Arena', 'price_in_Libreria_Palito', 'discount_Libreria_Palito', 'price_in_Libreria_Santa_Fe', 'discount_Libreria_Santa_Fe']
        wb = Workbook("negra.xlsx")

        for category, books in self.results.items():
            ws = wb.add_worksheet(category)
            first_row = 0
            for header in ordered_columns:
                col = ordered_columns.index(header) # We are keeping order.
                ws.write(first_row, col, header) # We have written first row which is the header of worksheet also.

            row = 1
            for book in books.values():
                # if there is no price, we don't want to include it
                if not book['Price']:
                    continue
                for _key,_value in book.items():
                    col = ordered_columns.index(_key)
                    ws.write(row, col, _value)
                row += 1 # enter the next row

        wb.close()
        
    def process_item(self, item, spider):
        if isinstance(item, SBook):
            self.handle_book(item, spider)
        return item
    
    def handle_book(self, item, spider):
        category_dict = self.results[item["category"]]
        primary_key = (item["title"], item["author"], item["category"])
                
        book_data = self.create_book_dict(item)
        if primary_key in category_dict:
            category_dict[primary_key] = {**category_dict[primary_key], **book_data}
        else:
            category_dict[primary_key] = book_data
            self.num_books += 1
            if self.num_books % 200 == 0:
                print(f"Processed {self.num_books} books, counts of each category: {[(k, len(v)) for k, v in self.results.items()]}")
        
    def create_book_dict(self, book_item):
        book_dict = {
            'Title': book_item['title'], 
            'Author': book_item['author'], 
            'Price': book_item['price'], 
            'Fecha Publicacion': book_item['fecha_publicacion'],
            'Idoma': book_item['idoma'],
            'ISBN': book_item['ISBN'],
            'Formato': book_item['formato'],
            'Presentacion': book_item['presentacion']
        }
        list_of_third_party_prices = book_item['third_party_prices']
        if list_of_third_party_prices:
            all_collected_names = []
            for price_item in list_of_third_party_prices:
                book_dict[f'price_in_{price_item["name"].replace(" ", "_")}'] = price_item['price']
                book_dict[f'discount_{price_item["name"].replace(" ", "_")}'] = price_item['discount']
                all_collected_names.append(price_item['name']) 
            not_collected = list(set(THIRD_PARTY_PLANETA) - set(all_collected_names))
            for name in not_collected:
                book_dict[f'price_in_{name.replace(" ", "_")}'] = None
                book_dict[f'discount_{name.replace(" ", "_")}'] = None
                
        return book_dict
