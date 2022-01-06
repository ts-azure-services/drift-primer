#!/bin/bash
grn=$'\e[1;32m'
end=$'\e[0m'

# Start of script
SECONDS=0
printf "${grn}STARTING 'workflow.sh' SCRIPT....${end}\n"
sleep 2

# Create resources
printf "${grn}RUNNING 'create-workspace-sprbac.sh SCRIPT....${end}\n"
./create-aml-resources.sh
sleep 15

# Create compute cluster
printf "${grn}CREATING A CLUSTER....${end}\n"
python clusters.py
printf "${grn}Giving about 60 seconds for the creation of the cluster to kick in....${end}\n"
sleep 15

# Upload datasets, and register them
printf "${grn}UPLOADING SAMPLE DATA AND REGISTERING IT AS A DATASET....${end}\n"
python datasets.py
sleep 15

duration=$SECONDS
printf "${grn} $duration SECONDS ELAPSED. CREATED THE WORKSPACE, LOADED THE DATASET, AND CREATED THE CLUSTER....${end}\n"

## Run basic pipeline script
#printf "${grn}RUN AUTOML PIPELINE SCRIPT....${end}\n"
#sleep 5
#python automl_pipeline.py
