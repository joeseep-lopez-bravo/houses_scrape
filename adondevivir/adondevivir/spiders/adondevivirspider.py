import scrapy
from scrapy import FormRequest

class AdondevivirspiderSpider(scrapy.Spider):
    name = "adondevivirspider"
    allowed_domains = ["adondevivir.com"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # 'HTTP_PROXY': 'http://your_proxy_address:port'
    }
    start_urls = ["https://adondevivir.com"]

    def start_requests(self):
        url = 'https://adondevivir.com'
        headers = {
            'Referer': 'https://www.adondevivir.com/'
        }
        # meta={'proxy': 'http://your_proxy_address:port'}
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extraer el token csrf si es necesario (no incluido en el código actual)

        # Crear el diccionario con los datos del formulario
        form_data = {
            'searchBox': 'huancayo',
            'propertyType': '2',
            'search-option': '1',
        }

        # Enviar el formulario con los datos especificados
        yield FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.procesar_resultados
        )

    def procesar_resultados(self, response):
        propiedades = response.css('.item-listing-wrap.hz-item-gallery-js.card')

        for propiedad in propiedades:
            propiedad_url = propiedad.xpath('.//h2/a/@href').get()
            yield response.follow(propiedad_url, callback=self.parse_propiedad_pagina)

        print(f"Processed URL: {response.url}")

    def parse_propiedad_pagina(self, response):
        # Aquí puedes extraer detalles adicionales de la propiedad individual si es necesario
        # Por ejemplo, título, descripción, precio, etc.
        pass
