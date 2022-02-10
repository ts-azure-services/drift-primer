#!/bin/bash
# Script to loop through iterations of data snapshots
grn=$'\e[1;32m'
end=$'\e[0m'

set -e

endpoint_script="./modeling/datamodeling/predict_against_baseline.py"

baseline_dataset="./datasets/baseline_revised.csv"

#names=("RETRAIN" "DATA-DRIFT" "CONCEPT-DRIFT")
names=("CONCEPT-DRIFT")

creation_script=(
	#"./modeling/retrain/create_retrain_dataset.py"
	#"./modeling/datadrift/create_datadrift_dataset.py"
	"./modeling/conceptdrift/create_concept_dataset.py"
	)

data_snapshot=(
	#"./datasets/retrain_data/retrain_dataset.csv"
	#"./datasets/ddrift_data/datadrift_dataset.csv"
	"./datasets/cdrift_data/concept_dataset.csv"
	)

# Get baseline accuracy
python $endpoint_script $baseline_dataset


#for (( i=0; i < ${#names[@]}; i++ ))
#do
#	for (( j=0; j<4; j++ ))
#	do
#		printf "${grn}CREATE DATASET FOR "${names[i]}"...${end}\n"
#		python "${creation_script[i]}"
#		sleep 2
#		printf "${grn}QUERY BASELINE ENDPOINT FOR "${names[i]}"...${end}\n"
#		python $endpoint_script "${data_snapshot[i]}"
#		sleep 2
#	done
#done
