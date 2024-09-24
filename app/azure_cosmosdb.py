import os
import json
import logging
import uuid
from datetime import datetime
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
        self.date = datetime.today().isoformat()

    def upload_files(self, paths):
        """Uploads JSON files to CosmosDB, based on a list of paths.

        Args:
            paths (list): A list of paths to files or directories.
        """
        for path in paths:
            if os.path.isfile(path):
                self.upload_file(path)
            elif os.path.isdir(path):
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    if filename.endswith('.json'):
                        self.upload_file(file_path)
            else:
                logging.error(f"Invalid path: {path}")

    def upload_file(self, file_path):
        """Uploads a single JSON file to CosmosDB.

        Args:
            file_path (str): The path to the JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'transcription' in data:
                self.insert_transcription(data, file_path)
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")

    def insert_transcription(self, data, filename):
        """Inserts transcription data into the CosmosDB container."""
        try:
            id = str(uuid.uuid4())
            transcricao_item = {
                'id': id,
                'prompt': data['prompt'],
                'audio_name': filename,
                'audio_path': data['audio_path'],
                'transcription': data['transcription'],
                'execution_date': self.date
            }
            self.container.create_item(body=transcricao_item)
            logging.info(f"Transcriptions inserted successfully for {id}")
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error inserting transcriptions for {id}: {e}")