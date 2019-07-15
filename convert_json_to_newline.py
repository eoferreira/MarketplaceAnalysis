import json

file='./input.json'
json_files = []
with open(file, 'r') as data_file:    
	new_json = json.load(data_file, encoding='utf8')
	output_newline = '\n'.join(map(lambda x: json.dumps(x, ensure_ascii=False), new_json))
	with open('./output.json', 'w') as outfile:
		outfile.write(output_newline)
