# azure_blob_downloader.py

from azure.storage.blob import BlobServiceClient, ContainerClient
import os

def download_blobs(connection_string, container_name, download_path):
    """
    Baixa blobs de um contêiner do Azure Blob Storage para um diretório local,
    evitando downloads repetidos verificando a pasta.

    Args:
        connection_string (str): A string de conexão do Azure Blob Storage.
        container_name (str): O nome do contêiner de origem.
        download_path (str): O caminho local para onde os blobs serão baixados.
    """

    os.makedirs(download_path, exist_ok=True)

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blobs_list = container_client.list_blobs()

    for blob in blobs_list:
        download_file_path = os.path.join(download_path, blob.name)

        blob_etag = container_client.get_blob_client(blob.name).get_blob_properties()

        if os.path.exists(download_file_path):
          continue


        print(f"Baixando blob para: {download_file_path}")
        with open(download_file_path, "wb") as download_file:
            download_file.write(container_client.download_blob(blob.name).readall())


    print("Download dos arquivos concluído!")