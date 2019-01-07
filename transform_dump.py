''' Created by Eduardo de Oliveira Ferreira @eoferreia
	Prepare extracted files to be ready for BigQuery injestion.
'''

import os
import json
from tqdm import tqdm

def ascii_encode_dict(data):
	'Prevents dictionary to be encoded as ascii'
	ascii_encode = lambda x: x.encode('utf-8') if type(x) is not int else str(x)
	return dict(map(ascii_encode, pair) for pair in data.items())


def formatInt(text):
	'When a string has numbers, removes characters and keep only numbers. Works with int values'
	if any(char.isdigit() for char in text):
		return int(''.join(filter(str.isdigit, text)))
	return text


def agglomerate(brand='', model=''):
	'Glue together all json files and generate a single newline json'
	path = './output/'
	if brand == '': # If user wants to get all files in all folders
		pass
	elif model == '': # If user wants to get all files from specific brand
		path += brand+'/'
	else:
		path += brand+'/'+model # If user wants to get files from specific car model

	f = []
	
	print('Getting file names')
	# Get all files and its paths	
	for (dirpath, dirnames, filenames) in tqdm(os.walk(path)):
		# f.extend([dirpath + '/' + file for file in filenames])
		f.extend(['{}/{}'.format(dirpath, file) for file in filenames])
	print('Transforming files')

	# Read files and generate json list
	json_files = []
	for file in tqdm(f):
		with open(file, 'r') as data_file:    
			new_json = json.load(data_file, encoding='utf8')
			# Do some transformations
			# Removing rows where seller didn't say the price
			if type(formatInt(new_json['preco'].replace('.', '').replace(',', '').replace('R$', ''))) is int:
				new_json['preco'] = new_json['preco'].replace('.', '').replace(',', '.').replace('R$', '')
				new_json['km'] = str(new_json['km'])
				new_json['ano'] = new_json['km'].replace(' ','')
				new_json['id'] = formatInt(new_json['id'])
				json_files.append(new_json)

	# Convert json list to newline json
	json_newline = [json.dumps(pos_json, ensure_ascii=False) for pos_json in json_files]

	if not os.path.exists('./bigquery/'):
		os.makedirs('./bigquery/')
	print('Saving output')
	output_newline = '\n'.join(json_newline)

	# Save to file (json is already encoded)
	with open('./bigquery/newline_{}_{}.json'.format(brand, model), 'w') as outfile:
		outfile.write(output_newline)
	print('DONE')


if __name__ == '__main__':
    # agglomerate('Chevrolet', 'Onix')
    agglomerate() # To get all files in all folders