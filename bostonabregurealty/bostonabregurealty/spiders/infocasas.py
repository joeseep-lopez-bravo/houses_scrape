import scrapy
import re
import json
from bostonabregurealty.items import BostonabregurealtyItem

class InfocasasSpider(scrapy.Spider):
    name = "infocasas"
    allowed_domains = ["infocasas.com.pe"]
    start_urls = [
        'https://www.infocasas.com.pe/venta/casas-y-departamentos/huancayo',
        'https://www.infocasas.com.pe/venta/casas-y-departamentos/junin/huancayo',
        'https://www.infocasas.com.pe/venta/casas-y-departamentos/huancayo/el-tambo',
        'https://www.infocasas.com.pe/venta/casas-y-departamentos/huancayo/pagina2'
    ]
    

    def parse(self, response):
         for url in self.start_urls:
            yield scrapy.Request(url, callback=self.procesar_resultados)

    def transform_text(self, complex_string):
        if complex_string:
                # Usar expresión regular para eliminar los comentarios HTML y extraer el texto
                string = re.sub(r'<!--.*?-->', '', complex_string)
                # Eliminar etiquetas HTML
                string = re.sub(r'<.*?>', '', complex_string)
                # Eliminar cualquier espacio en blanco adicional
                string = string.replace(" ", "")
        else:
                print("No se pudo extraer el string.")
                string = ""
 
        return string

    def procesar_resultados(self, response):
        properties= response.css('.listingCard.PE ')
       
        for property in properties:

            url_property= "https://www.infocasas.com.pe" +property.css('a::attr(href)').get()
            precio_bruto = property.css('div.lc-dataWrapper a.lc-data div.lc-price strong').get()
            precio =self.transform_text(precio_bruto)
            dormitorios=property.css('div.lc-dataWrapper a.lc-data div.lc-typologyTag strong::text').get()
            baños_bruto =property.css('div.lc-dataWrapper a.lc-data div.lc-typologyTag strong:nth-of-type(2)').get()
            area_bruto =property.css('div.lc-dataWrapper a.lc-data div.lc-typologyTag strong:nth-of-type(3)').get()
            detalle=property.css('div.lc-dataWrapper a.lc-data h2::text ').get()
            distrito=property.css('div.lc-dataWrapper a.lc-data strong.lc-location::text').get()
            area= self.transform_text(area_bruto)
            baños= self.transform_text(baños_bruto)
            
            if(response.status == 200):
                 print("nueva url a analizar: ", url_property)
                 yield scrapy.Request(url=url_property,meta={"distrito": distrito}, callback=self.parse_page_property)
            elif(response.status == 404):
                print("Página no encontrada (404): ", url_property)
                print("failed response", response.status)
                #print("failed response", type(response.status))
                self.logger.info(response.status)
                #property_item = BostonabregurealtyItem()
                #property_item['precio'] = precio
                #property_item['url'] = url_property
                #property_item['distrito'] = distrito
                #property_item['detalle'] = detalle
                #property_item['dormitorios'] = dormitorios
                #property_item['baños'] = baños
                #property_item['area'] = area
                pass
        

    def parse_page_property(self, response):
        distrito = response.meta["distrito"]
        lugar=response.css('h1.ant-typography.property-title::text').get()
        descripcion=response.css('div.ant-col.ant-col-24.padding.description-container div.ant-typography.property-description span::text').get()
        #dormitorio =response.css('div.ant-space-item span.ant-typography-ellipsis::text').get()
        precio=response.css('span.ant-typography.price strong::text').get()
        
        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(script_data)
        property_id = data['props']['pageProps']['__PROPERTY__ID__']
        
        #data1 = data['props']['pageProps']['apolloState'][f'Property:{property_id}']['technicalSheet']
        dormitorios = data['props']['pageProps']['apolloState'][f'Property:{property_id}']['bedrooms']
        cochera=data['props']['pageProps']['apolloState'][f'Property:{property_id}']['garage']
        baños = data['props']['pageProps']['apolloState'][f'Property:{property_id}']['bathrooms']
        area = data['props']['pageProps']['apolloState'][f'Property:{property_id}']['m2Built']
        floors = data['props']['pageProps']['apolloState'][f'Property:{property_id}']['technicalSheet']
        pisos_value = next((item["value"] for item in floors if item["field"] == "story"), None)
        pisos=pisos_value
        tipo_value= next((item["value"] for item in floors if item["field"] == "property_type_name"), None)
        tipo=tipo_value
        distrito = response.meta["distrito"]
        url = response.url

        propiedad_item = BostonabregurealtyItem()
        
        propiedad_item['url']=url
        print(url)
        propiedad_item['distrito']=distrito
        print(distrito)
        propiedad_item['lugar']=lugar
        print(lugar)
        #propiedad_item['dirección']= 
        propiedad_item['pisos']=pisos
        print(pisos)
        propiedad_item['tamaño']=area
        print(area)
        propiedad_item['tipo']=tipo
        print(tipo)
        propiedad_item['baños']=baños
        print(baños)
        propiedad_item['dormitorios']=dormitorios
        print(dormitorios)
        propiedad_item['precio']= precio
        print(precio)
        propiedad_item['detalle']= descripcion
        print(descripcion)
        propiedad_item['cochera']=cochera
        print(cochera)
        print("------------------------------")
        yield propiedad_item