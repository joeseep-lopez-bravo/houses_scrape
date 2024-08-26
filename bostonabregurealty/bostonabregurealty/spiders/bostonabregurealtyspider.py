import scrapy
from scrapy import FormRequest
from bostonabregurealty.items import BostonabregurealtyItem


class BostonabregurealtyspiderSpider(scrapy.Spider):
    name = "bostonabregurealtyspider"
    allowed_domains = ["bostonabregurealty.com"]
    start_urls = [""]


    def start_requests(self):
        url = 'https://bostonabregurealty.com'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        locations = ['Huancayo', 'El Tambo', 'Chilca', 'Huancán', 'Cajas']
        types = ['departamento', 'casas']
        for location in locations:
            for inmueble_type in types:
                formdata = {
                    'type[]': inmueble_type,  # Tipo de inmueble
                    'status[]': 'para venta',  # Venta / Alquiler
                    'location[]': location,    # Ciudad
                }
                # Log the form data being sent
                
                yield FormRequest.from_response(
                    response,
                    formid='houzez-search-3a474c0',
                    formdata=formdata,
                    callback=self.procesar_resultados
                )

    def procesar_resultados(self, response):
        propiedades = response.css('.item-listing-wrap.hz-item-gallery-js.card')
        
        for propiedad in propiedades:
            propiedad_url = propiedad.xpath('.//h2/a/@href').get()
            yield scrapy.Request(propiedad_url, callback=self.parse_propiedad_pagina, meta={'propiedad_url': propiedad_url})
        print(f"Processed URL: {response.url}")

    def parse_propiedad_pagina(self, response):
        propiedad_item = BostonabregurealtyItem()
        items = response.xpath('//*[@id="property-detail-wrap"]/div/div[2]/div/ul')
        cantidad_li = items.xpath('.//li')
        
        propiedad_item['direccion'] = response.css('.detail-address > span::text').get()
        detalle = response.xpath('//*[@id="property-description-wrap"]//text()').getall()
        propiedad_item['tipo'] = response.xpath('//li[@class="prop_type"]/span/text()').get()
        propiedad_item['distrito'] = response.css('.detail-city > span::text').get()
        propiedad_descripcion = response.xpath('//*[@id="main-wrap"]/section/div[2]/div/div[2]/div/h1/text()').get()
        
        propiedad_item['detalle'] = ''.join(detalle).replace('\n', ' ').replace('\t', '').strip()
        #print(f"Detalle: {propiedad_item['detalle']}")
        palabras = propiedad_descripcion.split()
        propiedad_item['lugar'] = ''

        for i, palabra in enumerate(palabras):
            if palabra == 'Urb.':
                propiedad_item['lugar'] = ' '.join(palabras[i:])
                break
        propiedad_item['pisos'] = ' '.join(palabras[:i])

        for li in range(1, len(cantidad_li) + 1):
            label = items.xpath(f'.//li[position()={li}]/strong/text()').get()
            span_text = response.xpath(f'.//*[@id="property-detail-wrap"]/div/div[2]/div/ul/li[position()={li}]/span/text()').get()
            if label and span_text:
                if 'tamaño' in label.lower():
                    propiedad_item['tamaño'] = span_text.strip()
                elif 'dormitorio' in label.lower():
                    propiedad_item['dormitorios'] = span_text.strip()
                elif 'cochera' in label.lower():
                    propiedad_item['cochera'] = span_text.strip()
                elif 'baño' in label.lower():
                    propiedad_item['baños'] = span_text.strip()
                elif 'precio' in label.lower():
                    propiedad_item['precio'] = span_text.strip()
        
        yield propiedad_item


