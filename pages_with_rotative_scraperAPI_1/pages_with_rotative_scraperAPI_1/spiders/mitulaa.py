import scrapy
from pages_with_rotative_scraperAPI_1.items import PagesWithRotativeScraperapi1Item

class MitulaaSpider(scrapy.Spider):
    name = "mitulaa"
    allowed_domains = ["casas.mitula.pe"]
    start_urls = ["https://casas.mitula.pe/casas/casas-huancayo",
                  ]

    def parse(self, response):
        properties=response.css('div#listings-content a')
        propiedad_item = PagesWithRotativeScraperapi1Item()
        for property in properties:
            url_property=property.css(' a::attr(href)').get()  
            if url_property:
             if url_property.startswith("/adform"):
                absolute_url = response.urljoin(url_property)
                yield scrapy.Request(absolute_url,callback=self.parse_item_page)
             elif url_property.startswith("/internal"):
               
                distrito=property.css('div.listing-card__title::text').get()
                precio=property.css('div.price::text').get()
                dormitorio=property.css('span[data-test="bedrooms"]::text').get()
                baño =property.css('span[data-test="bathrooms"]::text').get()
                area = property.xpath('.//div[contains(@class, "card-icon__area")]/following-sibling::span/text()').get()
                cochera =response.css('div.listing-card__facilities--separated div.facility-item span.facility-item__text:contains("Estacionamiento")').get()
                tipo=property.css('span.badge-container__property-type::text').get()
                img= response.css('div.photos img::attr(src)').get()
                if cochera :
                     cochera = 1
                else:
                     cochera = 0
                img=property.css('img::attr(content)').get()
                if not img:
                   img= property.css('img::attr(data-src)').get()
                print(img)            
                print('------------------------')
                propiedad_item['baños']=baño
                propiedad_item['url']=url_property
                print(response.url)
                propiedad_item['distrito']=distrito
                propiedad_item['tamaño']=area
                print('Área:', area)
                propiedad_item['tipo']=tipo
                propiedad_item['img']=img
                #print('Tipo:', tipo)
                #print('baño :', baños)
                propiedad_item['dormitorios']=dormitorio
                #print('dormitorios',dormitorio)
                propiedad_item['precio']= precio
                #print('el precio es :',price)
                #print('el detalle es :',detalle)
                propiedad_item['cochera']=cochera
                #print('cochera: ', cochera)
                print("------------------------------")    
                yield propiedad_item
        next_page_url=response.css('div.pagination__box a#pagination-next::attr(href)').get()
        if next_page_url is not None:
            yield response.follow(next_page_url,callback=self.parse)
    def parse_item_page(self,response):
        propiedad_item = PagesWithRotativeScraperapi1Item()
        price = response.css('div.prices-and-fees__price::text').get()
        lugar= response.css('div.main-title::text').get()
        tipo=response.css('div.property-type span.place-features__values::text').get()
        detalle= response.css('div#description-text::text').get()
        cochera = response.xpath('//ul[@class=" left-list"]/div[@class="facilities__item"]/li/span[contains(text(), "Estacionamiento")]').get()
        if cochera:
                 cochera = 1
        else:
                 cochera=0
        direccion=response.css('div.location-map__location-address-map::text').get()
        distrito= response.css('div.location::text').get()
        details_items = response.css('div.details-item')
        
        dormitorio = None
        baños = None
        area = None

        for item in details_items:
             icon = item.css('div.details-item-icon i.details-item__icon-bed[alt="bed"]')
             if icon:
                 dormitorio = item.css('div.details-item-value::text').get()
             
        for item in details_items:
             icon = item.css('div.details-item-icon i.details-item__icon-bath[alt="bath"]')
             if icon:
                 baños = item.css('div.details-item-value::text').get()
                 
                
        for item in details_items:
             icon = item.css('div.details-item-icon i.details-item__icon-area[alt="area"]')
             if icon:
                 area= item.css('div.details-item-value::text').get()

        print('------------------------')
        propiedad_item['baños']=baños
        propiedad_item['url']=response.url
        print(response.url)
        propiedad_item['distrito']=distrito
        #print('distrio: ',distrito)
        propiedad_item['lugar']=lugar
        #print('el lugar es: ', lugar)
        propiedad_item['direccion']=direccion
        #print('direcion: ',direccion)
        propiedad_item['tamaño']=area
        print('Área:', area)
        propiedad_item['tipo']=tipo
        #print('Tipo:', tipo)
        
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

             
        
             
           
