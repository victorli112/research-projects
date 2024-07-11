import unidecode
class PRHHelper:
    def __init__(self):
        self.title = None
        self.author = None
        self.price = None
        self.publication_date = None
        self.imprint = None
        self.prh_details = None
        
        # PRH details
        self.colleccion = None
        self.paginas = None
        self.target_de_edad = None
        self.tipo_de_encuadernacion = None
        self.idioma = None
        self.fecha_de_publicacion = None
        self.autor = None
        self.editorial = None
        self.referencia = None
        
    def populate_prh_basic_info(self, book_soup):
        self.title = book_soup.find('h1', class_="page-title").find('span').text.strip()
        self.author = book_soup.find('div', class_='autorYfav').find('a').text.strip()
        self.price = unidecode.unidecode(book_soup.find('span', class_='product-price').text.strip()).replace(' ','')

        # sometimes there wont be a publication date
        publication_date_element = book_soup.find('div', class_='product-category-name-editorial')
        if publication_date_element:
            self.publication_date= publication_date_element.text.split(',')[1].strip()
        else: 
            # we can get it from detailed info
            fecha_de_publicacion_tag = book_soup.find('dt', text='Fecha de publicación')
            if fecha_de_publicacion_tag:
                self.publication_date = fecha_de_publicacion_tag.find_next_sibling('dd').text.strip()
            else:
                self.publication_date = None
        
        imprint_element = book_soup.find('div', class_='product-category-name-editorial')
        if imprint_element:
            self.imprint = imprint_element.text.split(',')[0].strip()
    
    def populate_prh_detailed_info(self, book_soup):
        # Gather PRH details except reference number
        colleccion_tag = book_soup.find('dt', text='Colección')
        if colleccion_tag:
            self.colleccion = colleccion_tag.find_next_sibling('dd').text.strip()
        else:
            self.colleccion = None
        
        paginas_tag = book_soup.find('dt', text='Páginas')
        if paginas_tag:
            self.paginas = paginas_tag.find_next_sibling('dd').text.strip()
        else:
            self.paginas = None
        
        target_de_edad_tag = book_soup.find('dt', text='Target de Edad')
        if target_de_edad_tag:
            self.target_de_edad = target_de_edad_tag.find_next_sibling('dd').text.strip()
        else:
            self.target_de_edad = None
            
        tipo_de_encuadernacion_tag = book_soup.find('dt', text='Tipo de encuadernación')
        if tipo_de_encuadernacion_tag:
            self.tipo_de_encuadernacion = tipo_de_encuadernacion_tag.find_next_sibling('dd').text.strip()
        else:
            self. tipo_de_encuadernacion = None
            
        idoma_tag = book_soup.find('dt', text='Idioma')
        if idoma_tag:
            self.idioma = idoma_tag.find_next_sibling('dd').text.strip()
        else: 
            self.idioma = None 
            
        fecha_de_publicacion_tag = book_soup.find('dt', text='Fecha de publicación')
        if fecha_de_publicacion_tag:
            self.fecha_de_publicacion = fecha_de_publicacion_tag.find_next_sibling('dd').text.strip()
        else:
            self.fecha_de_publicacion = self.publication_date
            
        self.autor = self.author
        
        editorial_tag = book_soup.find('dt', text='Editorial')
        if editorial_tag:
            self.editorial = editorial_tag.find_next_sibling('dd').text.strip()
        else:
            self.editorial = None 
            
        # Get reference number 
        reference_number = book_soup.find('div', class_='product-reference')
        if reference_number:
            self.referencia = reference_number.find('span').text.strip()
        else:
            self.referencia = None
