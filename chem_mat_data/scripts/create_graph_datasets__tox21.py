import pandas as pd

from pycomex.functional.experiment import Experiment
from pycomex.utils import folder_path, file_namespace

from chem_mat_data import load_smiles_dataset

DATASET_NAME: str = 'tox21'

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
    We add the mol id fromt he dataset as additional metadata
    """
    graph['graph_id'] = data['mol_id']

@experiment.hook('load_dataset', default=False, replace=True)
def load_dataset(e: Experiment) -> dict[int, dict]:
    df = load_smiles_dataset('tox21')

    dataset: dict[int, dict] = {}
    # List of all 12 targets
    columns = ['NR-AR','NR-AR-LBD','NR-AhR','NR-Aromatase','NR-ER','NR-ER-LBD','NR-PPAR-gamma','SR-ARE','SR-ATAD5','SR-HSE','SR-MMP','SR-p53']
    for index, data in enumerate(df.to_dict('records')):
        
        data['smiles'] = data['smiles']
        # Is either 0 (inactive) , 1 (active) or no data given so -1
        data['targets'] = [(0 if data[col] == 0 else 1) if pd.notna(data[col]) else -1 for col in columns] 
        dataset[index] = data

    return dataset

experiment.run_if_main()

