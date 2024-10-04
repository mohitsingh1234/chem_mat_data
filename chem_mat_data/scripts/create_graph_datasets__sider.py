import os
import pandas as pd

from rich import print as pprint
from pycomex.functional.experiment import Experiment
from pycomex.utils import folder_path, file_namespace

from chem_mat_data import load_smiles_dataset

DATASET_NAME: str = 'sider'

__TESTING__ = False

experiment = Experiment.extend(
    'create_graph_datasets.py',
    base_path=folder_path(__file__),
    namespace=file_namespace(__file__),
    glob=globals(),
)

@experiment.hook('add_graph_metadata', default=False, replace=True)
def add_graph_metadata(e: Experiment, data: dict, graph: dict) -> dict:
    """
    No extra metadata
    """
    pass

@experiment.hook('load_dataset', default=False, replace=True)
def load_dataset(e: Experiment) -> dict[int, dict]:
    
    df = load_smiles_dataset('sider')
    dataset: dict[int, dict] = {}
    columns =["Hepatobiliary disorders","Metabolism and nutrition disorders","Product issues","Eye disorders","Investigations","Musculoskeletal and connective tissue disorders","Gastrointestinal disorders","Social circumstances","Immune system disorders","Reproductive system and breast disorders","Neoplasms benign or malignant and unspecified (incl cysts and polyps)","General disorders and administration site conditions","Endocrine disorders","Surgical and medical procedures","Vascular disorders","Blood and lymphatic system disorders","Skin and subcutaneous tissue disorders","Congenital or familial and genetic disorders","Infections and infestations","Respiratory or thoracic and mediastinal disorders","Psychiatric disorders","Renal and urinary disorders","Pregnancy or puerperium and perinatal conditions","Ear and labyrinth disorders","Cardiac disorders","Nervous system disorders","Injury or poisoning and procedural complications"]
     
    for index, data in enumerate(df.to_dict('records')):
        data['smiles'] = data['smiles']
        data['targets'] = [(0 if data[col] == 0 else 1) if pd.notna(data[col]) else -1 for col in columns]
        dataset[index] = data

    return dataset

experiment.run_if_main()
