import scrapy
from pages_with_rotative_scraperAPI_1.items import PagesWithRotativeScraperapi1Item
from  .config import API_KEY 

class TrovitSpider(scrapy.Spider):
    name = "trovit1"
    allowed_domains = ["casas.trovit.com.pe","rd.clk.thribee.com"]
    url_link='https://casas.trovit.com.pe/index.php/cod.search_homes/type.1/what_d.huancayo/isUserSearch.1'
    start_urls = ['http://api.scraperapi.com/?api_key='+ API_KEY + '&url=' + url_link + '&render=true']
        
    def parse(self, response):
        properties=response.css('div.snippet-wrapper.js-item-wrapper')
        for property in properties:
            url_property=property.css('div a::attr(href)').get()  
            if url_property:
             #print(f"Contenido del <li>: {url_property}")
             yield scrapy.Request(url_property,callback=self.parse_item_page)
           
        
        next_page_url=response.css('a.trovit-button.no-background.next[data-test="p-next"]::attr(href)').get()
        if next_page_url is not None:
            #print('------------------------------------------------------')
            #print('URL actual' , next_page_url)
            #print('------------------------------------------------------')
            #next_page='http://api.scraperapi.com/?api_key='+ API_KEY + '&url='+ next_page_url + '&render=true'
            
            yield response.follow(next_page_url,callback=self.parse) 
        

    def parse_item_page(self, response):
        print('-------------------------')
        propiedad_item = PagesWithRotativeScraperapi1Item()

        price= response.css('div.price span::text').get()
        dormitorio= response.xpath('//div[@id="amenities"]/ul/li[div[@class="amenity-key" and contains(text(),"Habitaciones")]]/div[@class="amenity-value"]/text()').get()
        baños= response.xpath('//div[@id="amenities"]/ul/li[div[@class="amenity-key" and contains(text(),"Baños")]]/div[@class="amenity-value"]/text()').get()
        
        distrito_full=response.css('div.address h2::text').get()
        if not distrito_full:
          # Si no se encuentra con el primer selector, intentar con 'h2.address::text'
          distrito_full = response.css('h2.address::text').get()
        distrito = ""
        direccion = ""
        if distrito_full:
            parts = distrito_full.split('  ')
            if len(parts) > 1:
                direccion = parts[0].strip()
                distrito = parts[1].strip()
            else:
                distrito = parts[0].strip()
                direccion ="" 
        
        tipo= response.xpath('//div[@id="amenities"]/ul/li[div[@class="amenity-key" and contains(text(),"Tipo de propiedad")]]/div[@class="amenity-value"]/text()').get()
        
        cochera = response.xpath('//ul[@class="facilities_list column-1"]/li[@class="facility"][contains(text(), "Cochera")]').get()
        if cochera:
            cochera = 1
        else:
            cochera = response.xpath('//ul/li[div[@class="amenity-key" and contains(text(), "Cochera")]]/div[@class="amenity-value"]/text()').get()
            if cochera:
                 cochera = 1
            else:
                cochera = 0 

        area=response.xpath('//div[@id="amenities"]/ul/li[div[@class="amenity-key" and contains(text(),"Superficie")]]/div[@class="amenity-value"]/text()').get()
        lugar=response.css('div.ap_traffic h1::text').get()
        if lugar is None:   
            lugar= response.css('div#main_info h1::text').get()
        detalle = response.css('div#description p::text').getall()

        
        print('------------------------')
        propiedad_item['url']=response.url
        print(response.url)
        propiedad_item['distrito']=distrito
        #print('distrio: ',distrito)
        propiedad_item['lugar']=lugar
        #print('el lugar es: ', lugar)
        propiedad_item['direccion']=direccion
        #print('direcion: ',direccion)
        propiedad_item['tamaño']=area
        #print('Área:', area)
        propiedad_item['tipo']=tipo
        #print('Tipo:', tipo)
        propiedad_item['baños']=baños
        #print('baño :', baños)
        propiedad_item['dormitorios']=dormitorio
        #print('dormitorios',dormitorio)
        propiedad_item['precio']= price
        #print('el precio es :',price)
        propiedad_item['detalle']= detalle
        #print('el detalle es :',detalle)
        propiedad_item['cochera']=cochera
        #print('cochera: ', cochera)
        print("------------------------------")
        yield propiedad_item
        
        
        
        
        
      
        