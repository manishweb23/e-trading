import requests
import gzip
from io import BytesIO
import hashlib
import config



def create_instruments():
    url = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv.gz"
    output_file_path = "NSE.csv"

    # Download the gzip file
    response = requests.get(url)

    if response.status_code == 200:
        # Decompress the gzip file
        compressed_data = BytesIO(response.content)
        with gzip.GzipFile(fileobj=compressed_data, mode='rb') as f:
            decompressed_data = f.read()

        # Write the decompressed data to a file
        with open(output_file_path, 'wb') as f_out:
            f_out.write(decompressed_data)

        print(f"File downloaded and saved as {output_file_path}")
        return "latest updated"
    else:
        print(f"Error downloading file. Status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return "somthing wrong!"


# create_instruments()

async def get_ltp(instrument_key):
    bearer_token = config.access_token

    # API endpoint
    api_url = 'https://api.upstox.com/v2/market-quote/ltp'

    # Set up headers with Bearer token
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }

    # Query parameters
    params = {
        'instrument_key': instrument_key,
    }

    # Make GET request
    response = requests.get(api_url, headers=headers, params=params)

    # Check the response
    if response.status_code == 200:
        data = response.json()
        print("Response:", data)
        return data
    else:
        print(f"Error: {response.status_code}")
        print("Response content:", response.text)
    return False


# Instrument key for NSE_FO|59268
instrument_key = 'NSE_FO|59268'
# instrument_key = 'NSE_EQ|INF179KC1965'
# get_ltp(instrument_key)


def md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()