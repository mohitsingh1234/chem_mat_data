# I aim to store the all the functions here.
import requests

def download_dataset(url, destination):
    # Makes a request to the above specified URL
    response = requests.get(url, stream = True)

    # Open the file..
    with open(destination, 'wb') as file:
        # .. and iterate over the contents of the file in little chunks.
        for chunk in response.iter_content(chunk_size=1024):
            # We check if it actually contains data and then write it to a file in a destination folder
            if chunk:
                file.write(chunk)


