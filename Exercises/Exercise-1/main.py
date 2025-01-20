import os
import requests
import shutil
import zipfile

VERBOSE = True

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def setup():
    _log('Setting up')
    for file in os.listdir('/Downloads'):
        _log(file)    
    if os.path.exists('/Downloads'):
        _log('/Downloads already exists')
        _log('Deleting all contents')
        shutil.rmtree('/Downloads')
    _log('Creating /Downloads')
    os.mkdir('/Downloads')

def download(link):
    assert isinstance(link, str)

    filename = link.split('/')[-1]
    _log(f'Downloading: {filename}')

    query_params = {'download_format': 'zip'}
    response = requests.get(link, params=query_params)
    if not response.ok:
        _log(f'{filename} not okay!')
        return

    filepath = '/Downloads/' + filename
    with open(filepath, mode='wb') as file:
        file.write(response.content)

def unzip(filename, parentdir):
    _log(f'unzipping {filename}')
    fullpath = parentdir + '/' + filename
    with zipfile.ZipFile(fullpath) as myzip:
        myzip.extractall(parentdir)

def _log(msg):
    if VERBOSE:
        print(msg)

def run():
    _log('run')
    setup()

    _log('downloading all')
    for link in download_uris:
        download(link)

    _log('unzipping')
    for filename in os.listdir('/Downloads'):
        unzip(filename, '/Downloads')

    _log('current file tree:')
    for file in os.listdir('/Downloads'):
        _log(file)

def main():
    _log('main')
    

if __name__ == "__main__":
    main()
