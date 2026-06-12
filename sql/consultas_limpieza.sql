-- BLOQUE 1: Promedio por categoria
SELECT 
	category,
	AVG(price) AS promedio_precio_por_categoria
FROM amazon_ecommerce 
GROUP BY 
	category
ORDER BY 
 	category DESC;

-- Filtro de riesgo - Punto crítico y KPI De Riesgo
SELECT 
 	delivery_status,
 	COUNT(*) AS cantidad_productos,
 	AVG(price) AS promedio_precios
FROM amazon_ecommerce
WHERE
 	category = 'Electronics' AND price > 42468.53138160097
GROUP BY
	delivery_status;

-- Productos Demorados, Entregados, Devueltos
SELECT 
	COUNT(*),
	AVG(is_returned::INTEGER) AS PROMEDIO,
	delivery_status
FROM amazon_ecommerce
WHERE category = 'Electronics'
GROUP BY 
	delivery_status;

-- Top 10 productos con más devoluciones
WITH conteo_devoluciones AS (
    SELECT 
        product_id,
        COUNT(*) AS total_devoluciones
    FROM amazon_ecommerce
    WHERE category = 'Electronics' 
      AND is_returned = TRUE
      AND price > 42468.53138160097
    GROUP BY product_id
),
ranking_productos AS (
    SELECT 
        product_id,
        total_devoluciones,
        RANK() OVER (ORDER BY total_devoluciones DESC) AS puesto_ranking
    FROM conteo_devoluciones
)
SELECT *
FROM ranking_productos
WHERE puesto_ranking <= 10;

-- Top 20 productos con mayores pérdidas por devoluciones
WITH lista_perdidas AS (
	SELECT 
		product_id,
		COUNT(*) AS total_devoluciones,
		AVG(price) AS precio_promedio
	FROM amazon_ecommerce
	WHERE category = 'Electronics' 
		AND is_returned = TRUE
	GROUP BY 
		product_id
),
Cantidad_devoluciones AS (
	SELECT 
		product_id,
		total_devoluciones,
		precio_promedio,
		RANK() OVER(ORDER BY precio_promedio DESC) AS ranking_resultados
	FROM lista_perdidas
)
SELECT *
FROM Cantidad_devoluciones 
WHERE ranking_resultados <= 20;

-- Análisis Geográfico: Top 500 por precio promedio
WITH Analisis_geografico AS (
	SELECT 	
		"location", 
		brand,
		subcategory,
		product_id,
		COUNT(*) AS total_devoluciones,
		delivery_status,
		AVG(price) AS precio_promedio
	FROM amazon_ecommerce
	WHERE category = 'Electronics'
		AND is_returned = TRUE
	GROUP BY 
		brand,
		subcategory,
		product_id,
		location,
		delivery_status
),
Resultados_ranking AS (
	SELECT 	
		brand,
		subcategory,
		precio_promedio,
		total_devoluciones,
		"location",
		RANK() OVER(ORDER BY precio_promedio DESC) AS ranking_precio_promedio
	FROM Analisis_geografico
)
SELECT *
FROM resultados_ranking
WHERE ranking_precio_promedio <= 500;

-- Mayor compras por dispositivos
SELECT 
    product_name,
    category,
    COUNT(*) AS total_de_compras,
    ROUND(AVG(final_price), 2) AS precio_promedio,
    ROUND(AVG(product_rating), 2) AS rating_promedio,
    SUM(CASE WHEN product_name = 'Web' THEN 1 ELSE 0 END) AS compras_web,
    SUM(CASE WHEN product_name = 'Mobile App' THEN 1 ELSE 0 END) AS compras_mobile,
    SUM(CASE WHEN product_name = 'Tablet' THEN 1 ELSE 0 END) AS compras_tablet
FROM ventas_ecommerce 
GROUP BY 
    category, 
    product_name;

-- Análisis por subcategoría, vendedor y ratings
SELECT 
	subcategory,
	category,
	seller_id,
	seller_rating,
	AVG(final_price) AS precio_final,
	product_rating 
FROM ventas_ecommerce 
GROUP BY
	category,
	product_rating,
	subcategory,
	seller_id,
	seller_rating
ORDER BY 
	product_rating DESC,
	seller_rating DESC,
	category DESC;
