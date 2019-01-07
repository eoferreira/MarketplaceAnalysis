from google.cloud import bigquery


def create_dataset(client, dataset_id):
	'Creates a dataset if not exists'
	datasets = list(client.list_datasets())
	project = client.project

	# Create a DatasetReference using a chosen dataset ID.
	# The project defaults to the Client's project if not specified.
	dataset_ref = client.dataset(dataset_id)

	if datasets:
	    print('\nDatasets in project {}:'.format(project))
	    for dataset in datasets:  # API request(s)
	        print('\t{}'.format(dataset.dataset_id))
	else:
	    print('\n{} project does not contain any datasets.'.format(project))


	# Construct a full Dataset object to send to the API.
	dataset = bigquery.Dataset(dataset_ref)
	# Specify the geographic location where the dataset should reside.
	dataset.location = "US"

	# Send the dataset to the API for creation.
	# Raises google.api_core.exceptions.Conflict if the Dataset already
	# exists within the project.
	try:
		print('Creating dataset \'{}\'...'.format(dataset_id))
		client.create_dataset(dataset)  # API request
		print('Dataset \'{}\' was created'.format(dataset_id))
		return client.dataset(dataset_id)
	except:
		print('Dataset \'{}\' already exists'.format(dataset_id))
		return client.dataset(dataset_id)


def create_table(client, dataset_ref, table_id, schema, autodetect=False):
	'Creates a table in the dataset if not exists'
	table_ref = dataset_ref.table(table_id)
	tables = list(client.list_tables(dataset_ref))  # API request(s)
	if tables:
	    print('\nTables in dataset {}:'.format(dataset_ref.dataset_id))
	    for table in tables:  # API request(s)
	        print('\t{}'.format(table.table_id))
	else:
	    print('\n{} dataset does not contain any tables.'.format(dataset_ref.dataset_id))

	try:
		print('Creating table \'{}\'...'.format(dataset_id))
		client.create_table(bigquery.Table(table_ref, schema=schema))                  # API request
		print('Table \'{}\' was created'.format(table_id))
		return dataset_ref.table(table_id)
		# return client.get_table(table_ref)
	except:
		print('Table \'{}\' already created'.format(table_id))
		return dataset_ref.table(table_id)


def load_data(client, dataset_ref, table_ref, filename):
	'Loads the data into a table in a dataset on bigquery'
	job_config = bigquery.LoadJobConfig()
	job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
	# job_config.skip_leading_rows = 1

	job_config.schema = schema
	# job_config.autodetect = True
	with open(filename, 'rb') as source_file:
	    job = client.load_table_from_file(
	        source_file,
	        table_ref,
	        location='US',  # Must match the destination dataset location.
	        job_config=job_config)  # API request
	try:
		print('Loading data...')
		job.result()  # Waits for table load to complete.
		print('Loaded {} rows into {}:{}.'.format(
	    		job.output_rows, dataset_id, table_id))
	except:
		print('An error ocurred when loading the data into the table')
		print(job.errors)


if __name__ == '__main__':
	# Connect to bigquery
	client = bigquery.Client.from_service_account_json('../../Downloads/ancient-medium-220620-dcb918ca109a.json')
	# client = bigquery.Client.from_service_account_json('../../Downloads/data-team-test-9679630f09ee (1).json')
	# Path to source file	
	filename = './bigquery/newline__.json'

	dataset_id = 'dataset_icarros'
	table_id = 'all_cars'
	schema = [
        bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('preco', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('titulo', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('marca', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('modelo', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('versao', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('cor', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('ano', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('link', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('transmissao', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('UF', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('cidade', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('bairro', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('anunciante', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('km', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('bool_particular', 'BOOLEAN', mode='REQUIRED')
    ]

	# Use the API to get references and load data
	dataset_ref = create_dataset(client, dataset_id)
	table_ref = create_table(client, dataset_ref, table_id, schema)
	load_data(client, dataset_ref, table_ref, filename)