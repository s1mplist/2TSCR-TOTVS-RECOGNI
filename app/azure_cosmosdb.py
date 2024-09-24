import argparse
import json
import logging
import os
import sys
import uuid
from azure.cosmos import CosmosClient, exceptions

class CosmosDBUploader:
    """A class for uploading JSON files to CosmosDB."""

    def __init__(self, cosmos_endpoint, cosmos_key, database_name, container_name):
        """Initializes the CosmosDBUploader object.

        Args:
            cosmos_endpoint (str): The CosmosDB endpoint.
            cosmos_key (str): The CosmosDB key.
            database_name (str): The name of the database.
            container_name (str): The name of the container.
        """
        self.client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    def upload_files(self, path):
        """Uploads JSON files to CosmosDB.

        Args:
            path (str): The path to the directory containing the JSON files.
        """
        for filename in os.listdir(path):
            logging.info(f"Processing file: {filename}")
            file_path = os.path.join(path, filename)

            if filename.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    try:
                        if 'transcription' in data:
                            self.insert_transcription(data, filename)
                    except Exception as e:
                        logging.error(f"Error processing file {filename}: {e}")

    def insert_transcription(self, data, filename):
        """Inserts transcription data into the CosmosDB container."""
        try:
            transcricao_item = {
                'id': str(uuid.uuid4()),
                'prompt': data['prompt'],
                'audio_name': filename,
                'audio_path': data['audio_path'],
                'transcription': data['transcription']
            }
            self.container.create_item(body=transcricao_item)
            logging.info(f"Transcriptions inserted successfully for {filename}")
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error inserting transcriptions for {filename}: {e}")