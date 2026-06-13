import os
import re
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "dbname": "simon_db",
    "user": "simon",
    "password": "simon123",
    "host": "localhost",
    "port": "5432"
}

def procesar_linea(linea, fila_idx):
    linea_limpia = linea.strip().strip('|')
    
    if not linea_limpia or '---' in linea_limpia or 'user_id' in linea_limpia or 'customer_id' in linea_limpia:
        return None
        
    if '|' in linea_limpia:
        datos = [col.strip() for col in linea_limpia.split('|')]
    elif '\t' in linea_limpia:
        datos = [col.strip() for col in linea_limpia.split('\t')]
    else:
        datos = [col.strip() for col in re.split(r'\s{2,}', linea_limpia)]
    
    # 1. Detectar y remover índice numérico al inicio (ej. '277')
    if len(datos) > 1 and datos[0].isdigit() and datos[1].startswith('U'):
        datos.pop(0)
    
    if len(datos) < 20:
        return None
        
    try:
        # 2. Auto-detectar si la marca viene duplicada en el texto (ej. 'Nike  Nike')
        try:
            float(datos[5].replace(',', '').strip())
            tiene_brand_clean = False
        except ValueError:
            tiene_brand_clean = True
            
        if tiene_brand_clean and len(datos) < 21:
            return None

        customer_id = datos[0]
        product_id  = datos[1]
        category    = datos[2]
        subcategory = datos[3]
        brand       = datos[4]
        
        # 3. Mapeo dinámico según la estructura detectada
        if tiene_brand_clean:
            brand_clean   = datos[5]
            precio        = float(datos[6].replace(',', '').strip())
            descuento     = float(datos[7].replace(',', '').strip())
            precio_final  = float(datos[8].replace(',', '').strip())
            rating        = float(datos[9])
            metric_a      = int(datos[10])
            metric_b      = int(datos[11])
            seller_id     = datos[12]
            seller_rating = float(datos[13])
            order_date    = datos[14]  
            quantity      = int(datos[15])
            city          = datos[16]
            product_name  = datos[17]  
            pay_method    = datos[18]
            is_returned   = datos[19].lower() == 'true'
            order_status  = datos[20]
        else:
            brand_clean   = brand
            precio        = float(datos[5].replace(',', '').strip())
            descuento     = float(datos[6].replace(',', '').strip())
            precio_final  = float(datos[7].replace(',', '').strip())
            rating        = float(datos[8])
            metric_a      = int(datos[9])
            metric_b      = int(datos[10])
            seller_id     = datos[11]
            seller_rating = float(datos[12])
            order_date    = datos[13]  
            quantity      = int(datos[14])
            city          = datos[15]
            product_name  = datos[16]  
            pay_method    = datos[17]
            is_returned   = datos[18].lower() == 'true'
            order_status  = datos[19]
            
        return (customer_id, product_id, category, subcategory, brand, brand_clean, 
                precio, descuento, precio_final, rating, metric_a, metric_b, 
                seller_id, seller_rating, order_date, quantity, city, 
                product_name, pay_method, is_returned, order_status)
                
    except Exception as e:
        print(f"[❌ Error en Fila {fila_idx}]: {e} | Datos iniciales: {datos[:3]}")
        return None

def pipeline_bulk_insert(ruta_archivo):
    query = """
        INSERT INTO ventas_ecommerce (
            customer_id, product_id, category, subcategory, original_brand, brand_clean,
            price, discount_percent, final_price, product_rating, metric_a, metric_b,
            seller_id, seller_rating, order_date, delivery_days, city, product_name,
            payment_method, is_premium, order_status
        ) VALUES %s;
    """
    buffer_registros = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for idx, linea in enumerate(f, 1):
                tupla_limpia = procesar_linea(linea, idx)
                if tupla_limpia:
                    buffer_registros.append(tupla_limpia)
            
        if not buffer_registros:
            print("[-] No se encontraron registros válidos.")
            return

        print(f"[+] Conectando a Postgres para cargar {len(buffer_registros)} filas...")
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                execute_values(cur, query, buffer_registros, page_size=1000)
                
        print("[¡ÉXITO!] Carga masiva finalizada correctamente.")
        
    except Exception as e:
        print(f"[-] Error crítico en el pipeline: {e}")

if __name__ == "__main__":
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_automatica = os.path.join(carpeta_actual, 'datos_prueba.txt')
    pipeline_bulk_insert(ruta_automatica)