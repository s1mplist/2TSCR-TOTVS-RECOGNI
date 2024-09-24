import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv(['STORAGE_ACCOUNT_KEY'])
reader = AzureBlobReader(connection_string)
reader.download_file("my-container", "my-file.txt", "local_file.txt")
content = reader.read_blob_content("my-container", "my-file.txt")
print(content)