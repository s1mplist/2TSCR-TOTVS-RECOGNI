import os
from azure.storage.blob import BlobServiceClient

class AzureBlobReader:
    """
    A class for reading files from Azure Blob Storage.
    """

    def __init__(self, connection_string):
        """
        Initializes the class with the Azure Storage connection string.

        Args:
            connection_string (str): The connection string for your Azure Storage account.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def download_file(self, container_name, blob_name, local_path):
        """
        Downloads a blob from Azure Blob Storage to a local file.

        Args:
            container_name (str): The name of the container.
            blob_name (str): The name of the blob.
            local_path (str): The local path where the file will be saved.
        """
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(local_path, "wb") as download_stream:
            download_stream.write(blob_client.download_blob().readall())

    def read_blob_content(self, container_name, blob_name):
        """
        Reads the content of a blob and returns it as a string.

        Args:
            container_name (str): The name of the container.
            blob_name (str): The name of the blob.

        Returns:
            str: The content of the blob.
        """
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        return blob_client.download_blob().readall().decode('utf-8')

    def download_file_to_specific_folder(self, container_name, blob_name, local_folder_path):
        """
        Downloads a blob from Azure Blob Storage to a specific local folder.

        Args:
            container_name (str): The name of the container.
            blob_name (str): The name of the blob.
            local_folder_path (str): The local path of the folder where the file will be saved.
        """
        # Create the folder if it doesn't exist
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        # Download the file to the specified folder
        local_file_path = os.path.join(local_folder_path, blob_name)
        self.download_file(container_name, blob_name, local_file_path)