import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os


class AzureBlobUploader:
    """
    A class for uploading files to Azure Blob Storage with logging capabilities.
    """

    def __init__(self, storage_account_key, container_name, log_level=logging.INFO, log_file=None):
        """
        Initializes the class with the storage account key, container name,
        optional log level, and log file path.

        Args:
            storage_account_key (str): The storage account key.
            container_name (str): The name of the Azure Blob Storage container.
            log_level (int, optional): The logging level (default: logging.INFO).
            log_file (str, optional): The file path for log messages (default: None).
        """

        load_dotenv()
        self.storage_account_key = storage_account_key
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.storage_account_key)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        if log_file:
            logging.basicConfig(filename=log_file, level=log_level)
        else:
            logging.basicConfig(level=log_level)  # Log to console by default

    def upload_file(self, file_path, overwrite=False):
        """
        Uploads a single file to the Azure Blob Storage container, handling existing blobs.

        Args:
            file_path (str): The path to the file to be uploaded.
            overwrite (bool, optional): Whether to overwrite an existing blob (default: False).

        Returns:
            bool: True if upload is successful, False otherwise.
        """

        filename = os.path.basename(file_path)
        blob_client = self.container_client.get_blob_client(filename)

        try:
            if not overwrite:
                self.logger.warning(f"Blob {filename} already exists. Skipping upload.")
                return False

            # If overwrite is True, delete the existing blob
            blob_client.delete_blob()
            self.logger.info(f"Overwriting existing blob {filename}")

        except Exception:
            # Blob doesn't exist, proceed with upload
            pass

        try:
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)

            self.logger.info(f"Upload do arquivo {filename} concluído!")
            return True

        except Exception as e:
            self.logger.error(f"Erro ao fazer upload do arquivo {filename}: {e}")
            return False

    def upload_files(self, file_paths, overwrite=False):
        """
        Uploads files from a list of paths to the Azure Blob Storage container, handling existing blobs.

        Args:
            file_paths (list): A list of file paths to be uploaded.
            overwrite (bool, optional): Whether to overwrite existing blobs (default: False).
        """

        for file_path in file_paths:
            self.upload_file(file_path, overwrite=overwrite)