import os
import json

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('utf-8') if type(x) is not int else str(x)
    return dict(map(ascii_encode, pair) for pair in data.items())

# json.loads(json_data, object_hook=ascii_encode_dict)

def formatInt(text):
	if any(char.isdigit() for char in text):
		return int(''.join(filter(str.isdigit, text)))
	return text

def agglomerate(brand='', model=''):
	path = './output/'
	if brand == '':
		pass
	elif model == '':
		path += brand+'/'
	else:
		path += brand+'/'+model+'/'

	f = []
	
	# Get all files and its paths	
	for (dirpath, dirnames, filenames) in os.walk(path):
		f.extend([dirpath + file for file in filenames])

	# Read files and generate json list
	json_files = []
	for file in f:
		with open(file, 'r') as data_file:    
			new_json = json.load(data_file, encoding='utf8')
			# Removing rows where seller didn't say the price
			if type(formatInt(new_json['preco'].replace('.', '').replace(',', '').replace('R$', ''))) is int:
				new_json['preco'] = new_json['preco'].replace('.', '').replace(',', '.').replace('R$', '')
				new_json['km'] = str(new_json['km'])
				new_json['id'] = formatInt(new_json['id'])
				json_files.append(new_json)
				# json_files[-1]['km'] = str(json_files[-1]['km'])
				# json_files[-1]['id'] = formatInt(json_files[-1]['id'])

			# json_files.append(json.loads(data_file.read().encode('utf-8').decode('unicode-escape')))#, object_hook=ascii_encode_dict))
			# json_files.append(json.loads(data_file.read().encode('utf-8').decode('unicode-escape'), object_hook=ascii_encode_dict))

	# print(json_files)
	# Convert json list to newline json
	json_newline = [json.dumps(pos_json, ensure_ascii=False) for pos_json in json_files]

	if not os.path.exists('./bigquery/'):
		os.makedirs('./bigquery/')

	output_newline = '\n'.join(json_newline)
	# print(output_newline)

	# Save to file (json is already encoded)
	with open('./bigquery/newline_{}_{}.json'.format(brand, model), 'w') as outfile:
		outfile.write(output_newline)

	# with open('./bigquery/newline_'+brand+'_'+model+'.json', 'w', encoding='utf8') as output:
	# 	json.dump('\n'.join(json_newline), output, ensure_ascii=False)


if __name__ == '__main__':
    agglomerate('Chevrolet', 'Onix')