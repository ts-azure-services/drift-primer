"""Script to upload CSV files"""
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws

def register_dataset(dataset=None, workspace=None, name=None, desc=None,tags=None):
    """Register datasets"""
    try:
        dataset = dataset.register(
                workspace=workspace, 
                name=name, 
                description=desc, 
                tags=tags,
                create_new_version=True
                )
        logging.info(f" Dataset registration successful for {name}")
    except Exception as e:
        logging.info(f" Exception in registering dataset. Error is {e}")

def upload_files_from_local(
        local_data_folder=None,
        target_def_blob_store_path=None,
        def_blob_store=None):
    """Function to upload files."""

    # Get input data files from local
    data_file_paths = data_filepaths(data_folder = local_data_folder)

    # Upload files to blob store
    def_blob_store.upload_files(
            files=data_file_paths,
            target_path=target_def_blob_store_path,
           overwrite=True,
            show_progress=True
            )

def main():
    """Set target locations, retrieve default blob store and upload files"""
    local_data_folder = './datasets/original/'
    target_def_blob_store_path = '/blob-input-data/'
    def_blob_store = ws.get_default_datastore()

    # Upload files
    upload_files_from_local(
            local_data_folder=local_data_folder,
            target_def_blob_store_path=target_def_blob_store_path,
            def_blob_store=def_blob_store
            )

    # Register the dataset
    datastore_paths = [(def_blob_store, str(target_def_blob_store_path))]
    fd = Dataset.Tabular.from_delimited_files(path=datastore_paths)
    register_dataset(dataset=fd, workspace=ws, name='Baseline Dataset')

if __name__ == "__main__":
    main()
