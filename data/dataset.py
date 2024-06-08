import os
import json
import yaml
import argparse
from kaggle.api.kaggle_api_extended import KaggleApi

def setup_kaggle_credentials(username, key):
    kaggle_dir = os.path.expanduser('~/.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)

    api_token = {"username": username, "key": key}
    with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
        json.dump(api_token, f)

    os.chmod(os.path.join(kaggle_dir, 'kaggle.json'), 0o600)

def download_dataset(dataset, destination):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=destination, unzip=True)

def main():
    parser = argparse.ArgumentParser(description="Download datasets from Kaggle based on a YAML configuration file.")
    parser.add_argument('config', type=str, help="Path to the YAML configuration file")

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    kaggle_credentials = config['kaggle_credentials']
    datasets = config['datasets']

    setup_kaggle_credentials(kaggle_credentials['username'], kaggle_credentials['key'])

    for dataset_info in datasets:
        dataset = dataset_info['dataset']
        destination = dataset_info['destination']
        download_dataset(dataset, destination)
        print(f"Dataset {dataset} downloaded to {destination}")

if __name__ == "__main__":
    main()
