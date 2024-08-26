    # Define your item pipelines here
    #
    # Don't forget to add your pipeline to the ITEM_PIPELINES setting
    # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
    # useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PagesWithRotativeScraperapi1Pipeline:
        def process_item(self, item, spider):
            adapter = ItemAdapter(item)
            # Procesar el campo 'precio'
            if 'precio' in adapter.field_names():
                precio_bruto = adapter.get('precio')
                logging.debug(f"Original 'precio' value: {precio_bruto}")
                if precio_bruto:  # Asegurarse de que 'precio' no sea None
                    precio_str = precio_bruto.replace('\n', '').replace(' ', '')
                    precio_str = precio_str.strip()
                    print("Cleaned 'precio' value:" + precio_str)
                    # Verificar si el precio está en dólares, euros o soles
                    try:
                        if 'U$S' in precio_str or '$' in precio_str or 'US$' in precio_str:
                            # Eliminar caracteres no numéricos excepto los puntos
                            precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                            # Convertir el separador de miles ('.') a una cadena vacía
                            precio_limpio = precio_limpio.replace('.', '')
                            # Convertir de dólares a soles (suponiendo una tasa de conversión de 3.6 soles por dólar)
                            precio = float(precio_limpio) * 3.6
                        elif '€' in precio_str:
                            # Eliminar caracteres no numéricos excepto los puntos
                            precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                            # Convertir el separador de miles ('.') a una cadena vacía
                            precio_limpio = precio_limpio.replace('.', '')
                            # Convertir de euros a soles (suponiendo una tasa de conversión de 4.1 soles por euro)
                            precio = float(precio_limpio) * 4.1
                        
                        elif 'USD' in precio_str:
                            # Eliminar caracteres no numéricos excepto los puntos
                            precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                            # Convertir el separador de miles ('.') a una cadena vacía
                            precio_limpio = precio_limpio.replace('.', '')
                            # Convertir de euros a soles (suponiendo una tasa de conversión de 4.1 soles por euro)
                            precio = float(precio_limpio) * 3.6
                        else:
                            # Eliminar caracteres no numéricos excepto los puntos y comas
                            precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c in ['.', ','])
                            # Convertir el separador de miles ('.') a una cadena vacía
                            precio_limpio = precio_limpio.replace('.', '').replace(',', '')
                            # Convertir a float directamente si está en soles
                            precio = float(precio_limpio)
                    
                            # Asignar el valor convertido al campo 'precio'
                            adapter['precio'] = precio
                    
                    except ValueError:
                        # Si no se puede convertir el precio a float, asignar un valor predeterminado
                        adapter['precio'] = None 
            # Limpiar saltos de línea en el campo 'detalle'
            if 'detalle' in adapter.field_names():
                detalle = adapter.get('detalle')
                
                if isinstance(detalle, list):
                    # Limpiar cada elemento de la lista
                    detalle_limpio = [texto.replace('\n', '').replace('\r', '').strip() for texto in detalle]
                    adapter['detalle'] = detalle_limpio
                elif isinstance(detalle, str):
                    # Limpiar el string directamente
                    adapter['detalle'] = detalle.replace('\n', '').replace('\r', '').strip()
            
            if 'dormitorios' in adapter.field_names():
                dormitorios_str = adapter.get('dormitorios')
                if dormitorios_str:  # Asegurarse de que 'dormitorios' no sea None
                    
                        # Eliminar caracteres no numéricos
                        dormitorios_limpio = ''.join(c for c in dormitorios_str if c.isdigit())
                        # Convertir a entero
                        dormitorios = int(dormitorios_limpio)
                        # Asignar el valor convertido al campo 'dormitorios'
                        adapter['dormitorios'] = dormitorios
            if 'baños' in adapter.field_names():
                baños_str = adapter.get('baños')
                if baños_str:  # Asegurarse de que 'dormitorios' no sea None
                        # Eliminar caracteres no numéricos
                        baños_limpio = ''.join(c for c in baños_str if c.isdigit())
                        # Convertir a entero
                        baños = int(baños_limpio)
                        # Asignar el valor convertido al campo 'dormitorios'
                        adapter['baños'] = baños

            if 'distrito' in adapter.field_names() or 'lugar' in adapter.field_names():
                distrito = adapter.get('distrito', '').strip().lower()
                lugar = adapter.get('lugar', '').strip().lower()
                lugares = ["el tambo", "chilca", "pariahuanca", "san agustín de cajas", "san agustin de cajas", "cajas", "pilcomayo"]
                found = False
                
                for lugar_buscar in lugares:
                    if lugar_buscar in distrito or lugar_buscar in lugar:
                        adapter['distrito'] = lugar_buscar.title()
                        found = True
                        break
                if not found:
                    if "pio pata" in distrito or "pio pata" in lugar:
                        adapter['distrito'] = "El Tambo"
                    elif any(term in distrito or term in lugar for term in ["san antonio", "merced", "rivera"]):
                        adapter['distrito'] = "Huancayo"
                    else:
                        adapter['distrito'] = "Huancayo"
            
                if 'tamaño' in adapter.field_names():
                    area_raw = adapter.get('tamaño')
                    if area_raw:
                        # Eliminar "m²" y cualquier espacio en blanco alrededor usando regex
                        area_cleaned = area_raw.replace('m²','').strip()
                        # Convertir a entero
                        area_cleaned = area_cleaned.replace(',', '')
                        try:
                            area_int = int(area_cleaned)  # Reemplazar ',' por '.' si es necesario
                            adapter['tamaño'] = area_int
                        except ValueError:
                            adapter['tamaño'] = None

            return item
            
