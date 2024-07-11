import unidecode
class PlanetaHelper:
    def __init__(self):
        self.title = None
        self.author = None
        self.price = None
        self.fecha_publicacion = None
        self.idoma = None
        self.ISBN = None
        self.formato = None
        self.presentacion = None
        
    def populate_planeta_basic_info(self, book_soup, title):
        title_block = book_soup.find('div', class_="product-bottom")
        if title_block:
            self.title = book_soup.find('div', class_="product-bottom").find('h1').text.strip()
        elif title:
            self.title = title
        else:
            raise Exception("No information for book")
        
        self.price = unidecode.unidecode(book_soup.find('span', class_='price-item--regular').text.strip()).replace(' ','')

        # assert the titles are the same 
        assert self.title.lower() == title.lower(), f"Title mismatch: {self.title.lower()} != {title.lower()}"
        
        author_tag = book_soup.find('td', text='Autor')
        if author_tag:
            self.author = author_tag.find_next_sibling('td').text.strip().replace('.','')
        
        fecha_publicacion_tag = book_soup.find('td', text='Fecha Publicación')
        if fecha_publicacion_tag:
            self.fecha_publicacion = fecha_publicacion_tag.find_next_sibling('td').text.strip()
        
        paginas_tag = book_soup.find('td', text='Páginas')
        if paginas_tag:
            self.paginas = paginas_tag.find_next_sibling('td').text.strip()
        
        idioma_tag = book_soup.find('td', text='Idioma')
        if idioma_tag:
            self.idoma = idioma_tag.find_next_sibling('td').text.strip()
        
        ISBN_tag = book_soup.find('td', text='ISBN')
        if ISBN_tag:
            self.ISBN = ISBN_tag.find_next_sibling('td').text.strip()
        
        formato_tag = book_soup.find('td', text='Formato')
        if formato_tag:
            self.formato = formato_tag.find_next_sibling('td').text.strip()
        
        presentacion_tag = book_soup.find('td', text='Presentación')
        if presentacion_tag:
            self.presentacion = presentacion_tag.find_next_sibling('td').text.strip()