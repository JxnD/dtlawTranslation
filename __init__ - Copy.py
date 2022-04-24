import logging
import string
import uuid
from azure.storage.blob import BlobServiceClient, __version__
from azure.core.exceptions import ResourceExistsError
from googletrans import Translator
import azure.functions as func


#translation function found from https://pypi.org/project/googletrans/3.1.0a0/
#block blob samples found from https://github.com/Azure/azure-sdk-for-python/blob/c80bd0e57eead32aad9ee1177f30332458050cdf/sdk/storage/azure-storage-blob/samples/blob_samples_hello_world.py#L27

connection_string = ''
translator = Translator()
translatestring = ''
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # Call translate function with input of httptrigger
        translatestring = translator.translate(name)
        # append output from translation function to blob storage
        block_blob_sample((f"Input Phrase: {translatestring.origin}." +'\n' + f"Translated from {translatestring.src} to {translatestring.dest}." + '\n' + f"Output Phrase: {translatestring.text}."))

        return func.HttpResponse(f"Input Phrase: {translatestring.origin}." +'\n' + f"Translated from {translatestring.src} to {translatestring.dest}." + '\n' + f"Output Phrase: {translatestring.text}.")
            
    else:
        return func.HttpResponse(
             "Please enter some input using ?name=",
             status_code=200
        )


def block_blob_sample(outputstring):

        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client("translatecontainer")

        try:
            # Create new Container in the service
            container_client.create_container()
        except ResourceExistsError as error:
                print(error)

        try:
            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client("translateoutput" + str(uuid.uuid4()))
            # Upload content to block blob
            blob_client.upload_blob(outputstring, blob_type="BlockBlob")
        finally:
            return func.HttpResponse("blob write failure")




