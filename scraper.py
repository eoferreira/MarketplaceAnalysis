''' Created by Eduardo de Oliveira Ferreira @eoferreia

'''

import requests
import os
import json
import math
from time import sleep
from bs4 import BeautifulSoup

# url = 'https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosNovos=1&anunciosUsados=1&marca1=5&modelo1=2428&anomodeloinicial=0&anomodelofinal=0&precominimo=0&precomaximo=0&cidadeaberto=&escopo=4&locationSop=cid_3382.1_-est_MG.1_-esc_2.1_-rai_50.1_'
# url = 'https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosNovos=1&anunciosUsados=1&marca1=35&modelo1=2417&anomodeloinicial=0&anomodelofinal=0&precominimo=0&precomaximo=0&cidadeaberto=Belo+Horizonte+-+MG&escopo=2&locationSop=cid_2754.1_-est_MG.1_-esc_2.1_-rai_50.1_'
# url = 'https://www.icarros.com.br//comprar/belo-horizonte-mg/toyota/etios-hatch?pag=3&ord=16'
url = 'https://www.icarros.com.br/comprar/chevrolet/onix'



base_url = 'https://www.icarros.com.br'


def formatText(text):

	# formattedText = text.replace(' ', '')\
	formattedText = " ".join(text.split())\
				    .replace('\r\n', '\n')\
				    .replace("\n", "")
	return formattedText

def save_json(data, path):
	if not os.path.exists(path):
		os.makedirs(path)
	with open(path+data['id']+'.json', 'w', encoding='utf8') as file:
		json.dump(data, file, ensure_ascii=False)

def formatInt(text):
	if any(char.isdigit() for char in text):
		return int(''.join(filter(str.isdigit, text)))
	return text


# def get_soup(content, parser='html.parser'):
# 	return

def parseAllAds(session, url='https://www.icarros.com.br/comprar/chevrolet/onix'):
	# Requests
	response = session.get(url)#, headers=headers)
	print(response)
	soup = BeautifulSoup(response.content, 'html.parser')
	# with open("output1.html", "w") as file:
	#     file.write(str(soup))
	# soup = BeautifulSoup(open("output1.html"), "html.parser")

	parent = soup.find('form', {'id': 'anunciosForm'})

	total_ads = soup.find('div', {'id': 'ctdoTitle'})\
					.find('h1', {'class': 'titulo'})\
					.find('span')\
					.getText()
	# print('Total de anúncios: {}'.format(int(''.join(filter(str.isdigit, total_ads)))))
	page_count = math.ceil(formatInt(total_ads)/20.0)

	print('Total de anúncios: {}'.format(formatInt(total_ads)))
	print('{} páginas'.format(page_count))
	curr_page = 1

	while response.status_code == 200:
		print('Parsing page {}/{}'.format(curr_page, page_count))
		print(url)
		parseAd(parent)
		curr_page += 1
		sleep(0.5)
		paging = soup.find('div', {'class': 'clearfix paginacao'})\
					 .find('li', {'class': 'proxima'})
		if paging != None:
			new_page = paging.find('a')\
					 		 .get('href')
			# print(new_page)
			url = base_url + new_page
			response = session.get(url)
			soup = BeautifulSoup(response.content, 'html.parser')
			parent = soup.find('form', {'id': 'anunciosForm'})
		else:
			print('Parsed last page!!')
			break
		# break
	else:
		print('Got a {} status_code'.format(response.status_code))


def parseAd(parent):
	# ul = parent.find('ul')
	anuncio_list = parent.find('ul')\
						 .findAll('li')


	for anuncio in anuncio_list:
		if anuncio.get('id') != None:
			# Save id
			ad_id = anuncio.get('id')
			# Find other data
			dados_veiculo = anuncio.find('div', {'class': 'dados_veiculo'})
			dados_a = dados_veiculo.find('a')
			# Save the link
			link = 'https://www.icarros.com.br'+dados_a.get('href')
			# Save the title
			title = dados_a.get('title')
			# Save manufacturer and model
			brand, version = title.split(' ', 1)
			model = version.split(' ', 1)[0]
			car_info = dados_a.find('ul', {'class': 'listahorizontal'}).findAll('li')

			color, year, km, transmission = '', '', '', ''
			for info in car_info:
				# Color
				if info.get('class') == []:
					if info.find('span').getText() == 'Cor':
						color = formatText( info.find('p').getText() )
					else:
						print('Error when reading color!')
				# Year
				elif info.get('class')[0] == 'primeiro':
					year = formatText( info.find('p').getText() )
				# Mileage
				elif info.get('class')[0] == 'zerokm':
					km = 0
				elif info.get('class')[0] == 'usado':
					km = formatInt( formatText( info.find('p').getText() ) )
				# Trasnmission
				elif info.get('class')[0] == 'ultimo':
					transmission = formatText( info.find('p').getText() )
				else:
					print('Error when reading car_info!!')


			###############################################################################3

			seller_data = anuncio.find('div', {'class': 'dados_anunciante'})
			dados_localizacao = seller_data.findAll('p')[-1]


			# If the neighborhood info is present
			if len(seller_data.findAll('p')) > 1:
				neighborhood = formatText( seller_data.findAll('p')[0].getText() )
			else:
				neighborhood = ''

			city = formatText( dados_localizacao.findAll('span')[0].getText() )
			state = formatText( dados_localizacao.findAll('span')[1].getText() )

			if seller_data.find('strong') == None:
				seller = seller_data.find('img').get('alt')
				bool_particular = 0
			else:
				seller = formatText( seller_data.find('strong').getText() )
				bool_particular = 1 

			################################################################################
			price = formatText( anuncio.find('h3', {'class': 'direita preco_anuncio'})\
								.getText()\
								.replace('R$', '') 
							  )
			data = {
	                'id': ad_id,
	                'preco': price,
	                'titulo': title,
	                'link': link,
	                'marca': brand,
	                'modelo': model,
	                'versao': version,
	                'cor': color,
	                'ano': year,
	                'km': km,
	                'transmissao': transmission,
	                'UF': state,
	                'cidade': city,
	                'bairro': neighborhood,
	                'anunciante': seller,
	                'bool_particular': bool_particular
	            }

			path = './output/{0}/{1}/'.format(brand, model)
			save_json(data, path)

if __name__ == '__main__':
    session = requests.Session()
    parseAllAds(session, url='https://www.icarros.com.br/comprar/chevrolet/onix?pag=68&ord=16')

