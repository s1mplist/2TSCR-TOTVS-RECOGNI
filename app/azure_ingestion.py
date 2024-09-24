import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

class AzureBlobStorageUploader:
    """
    A class for uploading files to Azure Blob Storage.
    """

    def __init__(self, storage_account_key, container_name):
        """
        Initializes the class with the storage account key and container name.

        Args:
            storage_account_key (str): The storage account key.
            container_name (str): The name of the Azure Blob Storage container.
        """
        load_dotenv()
        self.storage_account_key = storage_account_key
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(storage_account_key)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_files(self, file_type, path):
        """
        Uploads files of a specific type from a local directory to the Azure Blob Storage container.

        Args:
            file_type (str): The file type extension (e.g., ".wav", ".json", ".log").
            path (str): The local directory path containing the files to upload.
        """
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path) and filename.endswith(file_type):
                print(f"Lendo o arquivo: {filename}")

                blob_client = self.container_client.get_blob_client(filename)

                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data)

                print(f"Upload do arquivo {filename} concluído!")
            else:
                print(f"{filename} não é um arquivo {file_type} ou é um diretório.")


# Example usage
storage_account_key = os.environ['STORAGE_ACCOUNT_KEY']
container_audio = os.environ['CONTAINER_AUDIOS']
container_json = os.environ['CONTAINER_JSON']
container_logs = os.environ['CONTAINER_LOGS']

uploader = AzureBlobStorageUploader(storage_account_key, container_audio)
uploader.upload_files('.wav', './audio_samples/audio_samples')

uploader.container_name = container_json
uploader.upload_files('.json', './json_files')

uploader.container_name = container_logs
uploader.upload_files('.log', './logs')