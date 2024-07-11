import unidecode 

class ThirdPartyHelper:
    def __init__ (self):
        self.name = None
        self.price = None
        self.discount = None
    
    def populate_price(self, soup, url, book_title):
        if "www" in url:
            site_name = url.split('.')[1]
        else: 
            site_name = url.split('.')[0].split('//')[1]
        if site_name == "librenta":
            self.name = "Librenta"
            self.get_librenta_price(soup)
        elif site_name == "buscalibre":
            self.name = "Buscalibre"
            self.get_buscalibre_price(soup)
        elif site_name == "tematika":
            self.name = "Tematika"
            self.get_tematika_price(soup)
        elif site_name == "sbs":
            self.name = "SBS_Liberia"
            self.get_sbs_price(soup)
        elif site_name == "libreriahernandez":
            self.name = "Libreria_Hernandez"
            self.get_libreria_hernandez_price(soup)
        elif site_name == "cuspide":
            self.name = "Cuspide"
            self.get_cuspide_price(soup)
        elif site_name == "traslospasos":
            self.name = "Tras_los_Pasos"
            self.get_traslospasos_price(soup)
        else:
            raise Exception("Third party site not handled", book_title, site_name, url) 
        
        # normalize all values
        if self.name:
            self.name = unidecode.unidecode(self.name)
        if self.price:
            self.price = unidecode.unidecode(self.price).replace(' ','')
        if self.discount:
            self.discount = unidecode.unidecode(self.discount)
            
    def get_librenta_price(self, soup): 
        # Get price 
        price = soup.find('span', class_='andes-money-amount__fraction')
        if price:
            price = price.text
            self.price = "$" + price.strip()
        
        # No discount available
        
    def get_buscalibre_price(self, soup):
        # Get price 
        price = soup.find('p', class_='precioAhora')
        if price:
            self.price = price.find('span').text.strip()
            
        # Get discount if possible
        discount = soup.find('div', class_='box-descuento')
        if discount and discount.find('strong'):
            self.discount = discount.find('strong').text.strip()
        
    def get_tematika_price(self, soup):
        # Get discount if possible
        current_content_soup = soup.find('div', {"id": 'jm-current-content'})
        old_price = current_content_soup.find('p', class_='old-price')
        if old_price: 
            old_price = old_price.find('span', class_='price').text.strip()
            old_price_float = float(old_price.replace('$', '').replace('.', '').split(',')[0])
            curr_price = current_content_soup.find('p', class_='special-price').find('span', class_='price')
            if curr_price:
                curr_price = curr_price.text.strip()
                curr_price_float = float(curr_price.replace('$', '').replace('.', '').split(',')[0])
                discount = 1 - (curr_price_float / old_price_float)
                self.discount = str(round(discount * 100)).strip() + "%"
            else:
                raise Exception("Discount but no price")
            
        # No discount
        else:        
            price = current_content_soup.find('span', class_='regular-price')
            if price: 
                price = price.find('span', class_='price').text.strip()
                self.price = price
        
    def get_sbs_price(self, soup):
        # Get price 
        price = soup.find('span', class_='best-price')
        if price:
            price = price.text.strip()
            self.price = price
        
        # If there is a discount
        old_price = soup.find('span', class_='old-price')
        if old_price: 
            old_price = old_price.text
            old_price_float = float(old_price.replace('$', '').replace('.', '').split(',')[0])
            price_float = float(price.replace('$', '').replace('.', '').split(',')[0])
            discount = 1 - (price_float / old_price_float)
            self.discount = str(round(discount * 100)).strip() + "%"
    
    def get_libreria_hernandez_price(self, soup):
        # Get price 
        price = soup.find('td', class_='searchPrice')
        if price:
            self.price = price.text.strip()
                
    def get_cuspide_price(self, soup):
        price = soup.find('p', class_='product-page-price')
        if price and price.find('bdi'):
            price = price.find('bdi').text.strip()
            self.price = price
        
        # If there is a discount, find it and update price
        if soup.find('p', class_='price-on-sale'):
            discounted_price = soup.find('p', class_='price-on-sale').find_all('bdi')[1].text
            formatted_disc_price = float(discounted_price.replace('$', '').replace('.', '').split(',')[0])
            formatted_price = float(price.replace('$', '').replace('.', '').split(',')[0])
            discount = 1 - (formatted_disc_price / formatted_price)
            self.discount = str(round(discount * 100)).strip() + "%"
            self.price = discounted_price
                
    def get_traslospasos_price(self, soup):
        # Get price 
        price = soup.find('div', class_='item-description')
        if price:
            self.price = price.find('span', class_='item-price').text.strip()
    
    def __str__(self):
        return f'name={self.name}, price={self.price}, discount={self.discount}'
    
    def __repr__(self):
        return f'name={self.name}, price={self.price}, discount={self.discount}'
    
