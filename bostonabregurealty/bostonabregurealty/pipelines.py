# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BostonabregurealtyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Procesar el campo 'precio'
         # Procesar el campo 'precio'
        if 'precio' in adapter.field_names():
            precio_str = adapter.get('precio')
            
            # Verificar si el precio está en dólares, euros o soles
            if 'U$S' in precio_str or '$' in precio_str or 'US$' in precio_str:
                # Eliminar caracteres no numéricos excepto los puntos
                precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                # Convertir de dólares a soles (suponiendo una tasa de conversión de 3.6 soles por dólar)
                precio = float(precio_limpio) * 3.6
            elif '€' in precio_str:
                # Eliminar caracteres no numéricos excepto los puntos
                precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                # Convertir de euros a soles (suponiendo una tasa de conversión de 4.1 soles por euro)
                precio = float(precio_limpio) * 4.1
            else:
                # Eliminar caracteres no numéricos excepto los puntos y comas
                precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c in ['.', ','])
                # Reemplazar coma por punto para asegurar la conversión a float
                precio_limpio = precio_limpio.replace(',', '')
                # Convertir a float directamente si está en soles
                precio = float(precio_limpio)
            
            # Asignar el valor convertido al campo 'precio'
            adapter['precio'] = precio
        
        return item
        
       