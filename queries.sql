# By: Eduardo de Oliveira Ferreira

# Checking for duplicates
SELECT id, COUNT(id) FROM teste_scraper.teste_onix2 GROUP BY id HAVING COUNT(id) > 1;


#######################################################################################
# Produto: Onix

# Qual o preço médio do produto por cidade?
# Query que retorna preço médio de produto por cidade
SELECT cidade, UF, AVG(preco) as media
	FROM dataset_icarros.all_cars 
	WHERE modelo = 'Onix'
	GROUP BY cidade, UF
	ORDER BY cidade;

# Qual a cidade que possui mais ofertas do produto?
SELECT cidade, UF, COUNT(id) as total
	FROM dataset_icarros.all_cars 
	WHERE modelo = 'Onix'
	GROUP BY cidade, UF
	ORDER BY total DESC
	LIMIT 1;

# Liste os 5 mais baratos e o mais caro.
# 5 mais baratos:
SELECT versao, ano, km, cidade, UF, preco
	FROM dataset_icarros.all_cars 
	WHERE modelo = '{}'
	ORDER BY preco ASC
	LIMIT 5;

# Mais caro:
SELECT versao, ano, km, cidade, UF, preco
	FROM dataset_icarros.all_cars 
	WHERE modelo = '{}'
	ORDER BY preco DESC
	LIMIT 1;



#######################################################################################
# Produto: Todos os carros

# Qual o preço médio do produto por cidade?
# Query que retorna preço médio de produto por cidade
SELECT cidade, UF, AVG(preco) as media
	FROM dataset_icarros.all_cars 
	GROUP BY cidade, UF
	ORDER BY cidade;

# Qual a cidade que possui mais ofertas do produto?
SELECT cidade, UF, COUNT(id) as total
	FROM dataset_icarros.all_cars 
	GROUP BY cidade, UF
	ORDER BY total DESC
	LIMIT 1;

# Liste os 5 mais baratos e o mais caro.
# 5 mais baratos:
SELECT versao, ano, km, cidade, UF, preco
	FROM dataset_icarros.all_cars 
	ORDER BY preco ASC
	LIMIT 5;

# Mais caro:
SELECT versao, ano, km, cidade, UF, preco
	FROM dataset_icarros.all_cars
	ORDER BY preco DESC
	LIMIT 1;


#######################################################################################
# Queries extras - por curiosidade

# Query para verificar quantas cidades possuem anúncios:
SELECT COUNT (*) as total FROM (
	SELECT DISTINCT cidade, UF
		FROM dataset_icarros.all_cars 
		WHERE CIDADE IS NOT NULL 
			AND CIDADE <> ''
		GROUP BY cidade, UF
		ORDER BY cidade
);

# Query para verificar quantos estados possuem anúncios:
SELECT COUNT (*) as total FROM (
	SELECT DISTINCT UF
		FROM dataset_icarros.all_cars 
		WHERE UF IS NOT NULL 
			AND UF <> ''
		GROUP BY UF
		ORDER BY UF
);	

# Query para verificar quantos modelos diferentes possuem anúncios:
SELECT COUNT (*) as total FROM (
	SELECT DISTINCT modelo
		FROM dataset_icarros.all_cars 
		WHERE modelo IS NOT NULL 
			AND modelo <> ''
		GROUP BY modelo
		ORDER BY modelo
);

# Query para verificar quantos marcas diferentes possuem anúncios:
SELECT COUNT (*) as total FROM (
	SELECT DISTINCT marca
		FROM dataset_icarros.all_cars 
		WHERE marca IS NOT NULL 
			AND marca <> ''
		GROUP BY marca
		ORDER BY marca
);

# Query para verificar marca mais anunciada:
SELECT marca, COUNT(id) as total
	FROM dataset_icarros.all_cars
	GROUP BY marca
	ORDER BY total DESC
	LIMIT 1;

# Query para verificar modelo mais anunciado:
SELECT modelo, COUNT(id) as total
	FROM dataset_icarros.all_cars
	GROUP BY modelo
	ORDER BY total DESC
	LIMIT 1;