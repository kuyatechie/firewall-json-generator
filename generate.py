#!/usr/local/bin/python3

import argparse
import logging
import csv
import json

logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Python implementation of firewall json generator')

parser.add_argument('-s', '--source', metavar='PATH', dest='source', type=str, required=True,
                    help='The source csv file to refer the firewall configurations from.')

parser.add_argument('-f', '--filename', metavar='FILENAME', dest='filename', type=str, default='./output.json',
                     help='The source csv file to refer the firewall configurations from. '
                          'Default value is \'./output.json\'.')

parser.add_argument('-l', '--logfile', metavar='PATH', dest='logfile', type=str, default='./firewall-json-generator.log',
                    help='Path to logfile. Default value is \'./firewall-json-generator.log\'.')


class CSVFileHandler(object):
    def __init__(self, source_path):
        self.path = source_path

    def readFile(self):
        try:
            csv_file = open(self.path, mode='r', encoding='utf-8-sig')
            logger.info('Able to read csv file: {}'.format(self.path))
            return csv_file
        except Exception as e:
            logger.error('Error opening csv file. {}'.format(e))
            exit()

    def getDict(self):
        try:
            return csv.DictReader(self.readFile())
        except Exception as e:
            logger.error('Error converting csv to dictionary. {}'.format(e))
            exit()

    def getJSON(self):
        try:
            return json.dumps([row for row in self.getDict()], indent=4, sort_keys=True)
            logger.info('Able to convert csv to JSON')
        except Exception as e:
            logger.error('Error converting dictionary to json. {}'.format(e))
            exit()

class FileGenerator(object):
    def __init__(self, json_string, destination_path):
        self.path = destination_path
        self.content = json_string

    def writeToFile(self):
        try:
            target_file = open(self.path, 'w')
            target_file.write(self.content)
            logger.info('Able to write to file: {}'.format(self.path))

        except Exception as e:
            logger.error('Error writing to target json path. {}'.format(e))
            exit()


if __name__ == '__main__':
    # Initiate argument parser
    args = parser.parse_args()

    # Initiate logging module
    streamhandler = logging.StreamHandler()
    filehandler = logging.FileHandler(filename=args.logfile)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    streamhandler.setFormatter(formatter)
    filehandler.setFormatter(formatter)

    logger.addHandler(streamhandler)
    logger.addHandler(filehandler)
    logger.setLevel(logging.INFO)

    # Read and convert CSV file
    csv_handler = CSVFileHandler(source_path=args.source)
    json_output = csv_handler.getJSON()

    # Write to JSON file
    file_generator = FileGenerator(json_string=json_output, destination_path=args.filename)
    file_generator.writeToFile()
