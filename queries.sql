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
	LIMIT 5

# Mais caro:
SELECT versao, ano, km, cidade, UF, preco
	FROM dataset_icarros.all_cars
	ORDER BY preco DESC
	LIMIT 1