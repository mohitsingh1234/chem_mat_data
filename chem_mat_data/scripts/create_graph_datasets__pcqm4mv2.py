from pycomex.functional.experiment import Experiment
from pycomex.utils import folder_path, file_namespace

from chem_mat_data import load_smiles_dataset

DATASET_NAME: str = 'pcqm4mv2'

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
    There is no additional metadata to be added for this dataset
    """
    pass
@experiment.hook('load_dataset', default=False, replace=True)
def load_dataset(e: Experiment) -> dict[int, dict]:
    df = load_smiles_dataset('pcqm4mv2')
    dataset: dict[int, dict] = {}
    for index, data in enumerate(df.to_dict('records')):
        data['smiles'] = data['SMILES']
        data['targets'] = data['Target']
        dataset[index] = data

    return dataset

experiment.run_if_main()
