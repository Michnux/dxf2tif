#freely inspired from https://github.com/alteia-ai/rust-detector/blob/master/detect_rust.py#L5
import json
import logging
import os
from pathlib import Path
import sys
from dxf2tif import dxf2tif

import time

from upload_dataset import upload_dataset


LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)



def load_inputs(input_path):
	inputs_desc = json.load(open(input_path))
	inputs = inputs_desc.get('inputs')
	parameters = inputs_desc.get('parameters')
	return inputs, parameters


def main():

	SCRIPT_DIR = Path(__file__).parent.resolve()
	WORKING_DIR = os.getenv('DELAIRSTACK_PROCESS_WORKDIR')
	if not WORKING_DIR:
		raise KeyError('DELAIRSTACK_PROCESS_WORKDIR environment variable must be defined')
	WORKING_DIR = Path(WORKING_DIR).resolve()

	logging.debug('WORKING_DIR :')	
	logging.debug(WORKING_DIR)


	logging.debug('Extracting inputs and parameters...')
	# Retrieve inputs and parameters from inputs.json
	inputs, parameters = load_inputs(WORKING_DIR / 'inputs.json')

	logging.debug('inputs :')	
	logging.debug(inputs)
	logging.debug('parameters :')	
	logging.debug(parameters)

	# file_path = WORKING_DIR / inputs.get('input_pc').get('components')[0]['filename']
	file_path = inputs.get('input_dxf').get('components')[0]['path']
	project_id = inputs.get('input_dxf').get('project')
	mission_id = inputs.get('input_dxf').get('mission')
	grid_size = parameters.get('grid_size') #str or None
	if not grid_size:
		grid_size = 0.2
	else:
		grid_size = float(grid_size) #to float

	logging.debug(file_path)
	logging.debug(grid_size)


	dxf2tif(file_path, grid_size, WORKING_DIR)


	logging.debug('Generating outputs.json file...')

	outpath = WORKING_DIR / 'output.tif'
	output = {
		"outputs": {
			"outputtif": {  # Must match the name of deliverable in rust-detector.yaml
				"type": "raster",
				"format": "tif",
				# "categories": [],
				"name": "outputtif",
				"components": [
					{
						"name": "raster",
						# "filename": "output.tif",
						"path": str(outpath)
					}
				]
			}
		},
		"version": "0.1"
	}
	with open(WORKING_DIR / 'outputs.json', 'w+') as f:
		json.dump(output, f)

	logging.debug('End.')




if __name__ == "__main__":

	main()