import os
import requests
import click
from utility import download_dataset
from datasets import available_datasets


#This script runs the following way:
#In terminal type "python3 prototype_pipeline.py [name of dataset]"
#Right now there are only two datasets uploaded, HIV.csv and toxcast_data.csv
#Thus one has to execute "python3 prototype_pipeline.py HIV" if interested in that dataset.
#The .csv can be omitted.
#The names of the datasets were taken as given in original form.
# Where the datasets are stored
base_url = 'https://bwsyncandshare.kit.edu/s/egMpWo6KiBRQGdF/download?path=%2F&files='

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('filename', type=str, required=False)
@click.option('-check', is_flag=True, help= 'List available datasets')
@click.option('-a', is_flag=True, help = 'Downloads all available datasets')
def main(filename, check, a):
    """
    Prototype Pipeline: A tool for downloading datasets.

    To download a dataset, provide its name as an argument. 
    For example: python3 pipeline.py HIV
    """

    if a:
        click.confirm('This will donwload the whole collection of datasets to your current working directory. Are you sure?', abort=True)
        try:
            download_dataset(base_url, 'Dataset.zip')
            click.echo(f'Collection downloaded succesfully')
        except Exception as e:
            logging.error(f'Error downloading collection : {e}')
            click.echo(f'Failed to download collection: {e}')
        return
    #This will print out the available datasets
    if check:
        click.echo('Available datasets:')
        for dataset in available_datasets:
            click.echo(dataset)
        return

    #If no argument is provided, it will prompt the user to give one or use an option flag
    if not filename:
        click.echo('Please provide a dataset name or use the "check" option to see available datasets or use "--help" option.')
        return
    
    #Strip it of whitespace 
    filename = filename.strip()

    # We need to check if the dataset actually exists
    if filename not in available_datasets:
        click.echo(f'Dataset {filename} not found. Available datasets can be seen via "-check" option')
        return
    
    ### From here on out, the code aims to download the file as specified by the user ####
    
    # Add the ".csv" extension, wich is needed to construct the url
    filename = filename if filename.endswith('.csv') else f'{filename}.csv'
    # Create 'datasets' folder if it doesn't exist. All datasets are stored in that folder
    datasets_folder = 'datasets'
    if not os.path.exists(datasets_folder):
        os.makedirs(datasets_folder)

    # This is the path where the dataset will be
    destination = os.path.join(datasets_folder, filename)
    if os.path.exists(destination):
        click.confirm('File already exists. Do you want to overwrite?', abort=True)

    # Determine the url for the dataset
    dataset_url = base_url + filename
    try:
        download_dataset(dataset_url, destination)
        click.echo(f'Dataset downloaded succesfully to {destination}')
    except Exception as e:
        logging.error(f'Error downloadign dataset: {e}')
        click.echo(f'Failed to download dataset: {e}')

if __name__ == '__main__':
    main()
