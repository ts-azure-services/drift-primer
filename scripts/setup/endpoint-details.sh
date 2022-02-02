#!/bin/bash
#Script to provision a new Azure ML workspace
grn=$'\e[1;32m'
end=$'\e[0m'

set -e

# Start of script
SECONDS=0
printf "${grn}STARTING RETRIEVAL OF ENDPOINT DETAILS...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Resource and workspace details
resourcegroup='mlops_primer1781'
workspacename='mlops_primer1781workspace'

# Get baseline endpoint details
printf "${grn}GET BASELINE ENDPOINT URI...${end}\n"
baseline_endpoint_name='baseline-model-endpoint'
baseline_uri=$(az ml online-endpoint show\
	--name $baseline_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "scoring_uri")
printf "Result of baseline URI:\n $baseline_uri \n"
sleep 2

printf "${grn}GET BASELINE ENDPOINT API KEY...${end}\n"
baseline_apikey=$(az ml online-endpoint get-credentials\
	--name $baseline_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "primaryKey")
printf "Result of baseline api key:\n $baseline_apikey \n"
sleep 2

# Get retrain endpoint
printf "${grn}GET RETRAIN ENDPOINT URI...${end}\n"
retrain_endpoint_name='retrain-endpoint'
retrain_uri=$(az ml online-endpoint show\
	--name $retrain_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "scoring_uri")
printf "Result of retrain URI:\n $retrain_uri \n"
sleep 2

printf "${grn}GET RETRAIN ENDPOINT API KEY...${end}\n"
retrain_apikey=$(az ml online-endpoint get-credentials\
	--name $retrain_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "primaryKey")
printf "Result of retrain api key:\n $retrain_apikey \n"
sleep 2


# Get concept drift endpoint
printf "${grn}GET CONCEPT ENDPOINT URI...${end}\n"
concept_endpoint_name='cdrift-endpoint'
concept_uri=$(az ml online-endpoint show\
	--name $concept_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "scoring_uri")
printf "Result of concept URI:\n $concept_uri \n"
sleep 2

printf "${grn}GET CONCEPT ENDPOINT API KEY...${end}\n"
concept_apikey=$(az ml online-endpoint get-credentials\
	--name $concept_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "primaryKey")
printf "Result of concept api key:\n $concept_apikey \n"
sleep 2


# Get data drift endpoint
printf "${grn}GET DDRIFT ENDPOINT URI...${end}\n"
ddrift_endpoint_name='ddrift-endpoint'
ddrift_uri=$(az ml online-endpoint show\
	--name $ddrift_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "scoring_uri")
printf "Result of ddrift URI:\n $ddrift_uri \n"
sleep 2

printf "${grn}GET DDRIFT ENDPOINT API KEY...${end}\n"
ddrift_apikey=$(az ml online-endpoint get-credentials\
	--name $ddrift_endpoint_name \
	-g $resourcegroup \
	--workspace-name $workspacename \
	--query "primaryKey")
printf "Result of ddrift api key:\n $ddrift_apikey \n"
sleep 2


# Create endpoint file
printf "${grn}WRITING OUT ENDPOINT DETAILS....${end}\n"
env_variable_file='endpoint_details.env'
printf "BASELINE_URI=$baseline_uri \n" > $env_variable_file
printf "BASELINE_APIKEY=$baseline_apikey \n" >> $env_variable_file
printf "RETRAIN_URI=$retrain_uri \n" >> $env_variable_file
printf "RETRAIN_APIKEY=$retrain_apikey \n" >> $env_variable_file
printf "CDRIFT_URI=$concept_uri \n" >> $env_variable_file
printf "CDRIFT_APIKEY=$concept_apikey \n" >> $env_variable_file
printf "DDRIFT_URI=$ddrift_uri \n" >> $env_variable_file
printf "DDRIFT_APIKEY=$ddrift_apikey \n" >> $env_variable_file
