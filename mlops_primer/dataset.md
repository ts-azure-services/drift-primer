# The Dataset
This dataset captures customer and feature attributes around use of telecom solution, which was sourced from
this [Kaggle
repo](https://www.kaggle.com/blastchar/telco-customer-churn?select=WA_Fn-UseC_-Telco-Customer-Churn.csv). This
is originally sourced as part of IBM samples
[here](https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113).
The general description reads: *"The Telco customer churn data contains information about a fictional telco
company that provided home phone and Internet services to 7043 customers in California in Q3. It indicates
which customers have left, stayed, or signed up for their service."*

Effectively, this data represents a snapshot in time or the install base of the fictional company at a point
in time. 'Churn' is also a point in time evaluation and is an estimation of the customer engagement at a point
in time. For the purposes of this case study, we assume that once a customer is churned, they do not return.
We also trust that the company adequately has a rigorous process for classifying a customer as 'Churned'.

For the ML model, we will be predicting churn. Note that for many organizations, predicting churn is not an
end goal in itself. Instead, many would prefer to focus on customer retention. For the purposes of this case
study, we assume that predicting churn is a needed step in the process to evaluate and diagnose accurately
where underlying problems may exist, including those that have short-term as well as longer term resolutions.

## Registering the Dataset
Note that as part of data lineage, it is a good practice to register a dataset as part of the initial training
process. Datasets can be sourced from Azure Storage blobs, ADLS, and a variety of operational datastores (SQL
DB, PostgreSQL and MySQL). For the purposes of this case study, the original dataset will be uploaded from our
local drive as part of the initial workspace, and infrastructure creation process.

Code snippets of that process include:

Finding the filepaths in the local folder
```python
def data_filepaths(data_folder=None):
    """Get full paths to discrete data files"""
    full_filepaths = []
    absolute_path = Path(data_folder).absolute()
    data_files = os.listdir(data_folder)
    for file in data_files:
        file_with_path = str(absolute_path) + '/' + str(file)
        full_filepaths.append(file_with_path)
    return full_filepaths
```

Registering the dataset
```python
def register_dataset(dataset=None, workspace=None, name=None, desc=None,tags=None):
    """Register datasets"""
    try:
        dataset = dataset.register(workspace=workspace,name=name,description=desc,tags=tags,create_new_version=True)
        print(f" Dataset registration successful for {name}")
    except Exception as e:
        print(f" Exception in registering dataset. Error is {e}")
```

Retrieving the default datastore, and uploading the files 
```python
def main():
    """Main operational flow"""
    # Set target locations and specific filename
    local_data_folder = './../input-data'
    target_def_blob_store_path = '/blob-input-data/'
    input_filename = 'HPI_master.csv'

    # Get input data files from local
    data_file_paths = data_filepaths(data_folder = local_data_folder)

    # Get the default blob store
    def_blob_store = ws.get_default_datastore()

    # Upload files to blob store
    def_blob_store.upload_files(
            files=data_file_paths, 
            target_path=target_def_blob_store_path,
            overwrite=True,
            show_progress=True
            )
    
    # Create File Dataset
    datastore_paths = [(def_blob_store, str(target_def_blob_store_path + input_filename))]
    fd = Dataset.File.from_files(path=datastore_paths)
```


## Dataset Profile
It is helpful to take advantage of the 'dataset profile' tool that exists in the Dataset section of Azure
Machine Learning. This helps data scientists quickly assess data completeness and the type, and range of
values for a given attribute.
<span style="color:red">**show example**</span>

- Max tenure is 72 months or 6 years.
