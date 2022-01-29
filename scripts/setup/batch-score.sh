#!/bin/bash
#Script to provision a new Azure ML workspace
grn=$'\e[1;32m'
end=$'\e[0m'

set -e
# Start of script
printf "${grn}STARTING CREATION OF BATCH DEPLOYMENT...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Set the workspace, RG and location defaults
az configure --defaults \
	group="mlops_primer2937"\
	workspace="mlops_primer2937workspace"\
	location="westus"

# Get endpoint name
dep_number=$[ ( $RANDOM % 10000 ) + 1 ]
ENDPOINT_NAME='dep'$dep_number
printf "${grn}ENDPOINT_NAME IS $ENDPOINT_NAME...${end}\n"

## Create AML compute
#cluster_name='batch'$dep_number
#az ml compute create \
#	-n $cluster_name \
#	--type amlcompute \
#	--min-instances 0 \
#	--max-instances 5

# Create the batch endpoint
az ml batch-endpoint create \
	--file './scripts/setup/endpoint.yml' \
	--resource-group "mlops_primer2937"\
	--workspace-name "mlops_primer2937workspace"

# Create batch deployment
az ml batch-deployment create \
	--file './scripts/setup/deployment.yml' \
	--name nonmlflowdp \
	#--endpoint-name $ENDPOINT_NAME \
	--endpoint-name "endpoint42" \
	--resource-group "mlops_primer2937"\
	--workspace-name "mlops_primer2937workspace"
	#--set-default

# Start batch scoring job
JOB_NAME=$(az ml batch-endpoint invoke \
	--name $ENDPOINT_NAME \
	--input-path folder:https://mlopspristorage09ec356dd.blob.core.windows.net/azureml-blobstore-934b57e9-ee4b-4420-b02d-2f9c8cccb6b2/managed-dataset/6ba0c119-e7cf-4a48-b825-a2217743b150/part-00000.parquet
)
printf "Result of job execution: \n $JOB_NAME \n"


## Source unique name for RG, workspace creation
#unique_name='mlops_primer'
#number=$[ ( $RANDOM % 10000 ) + 1 ]
#resourcegroup=$unique_name$number
#workspacename=$unique_name$number'workspace'
#location='westus'
#
## Create a resource group
#printf "${grn}STARTING CREATION OF RESOURCE GROUP...${end}\n"
#rg_create=$(az group create --name $resourcegroup --location $location)
#printf "Result of resource group create:\n $rg_create \n"
#
## Create workspace through CLI
#printf "${grn}STARTING CREATION OF AML WORKSPACE...${end}\n"
#ws_result=$(az ml workspace create -w $workspacename -g $resourcegroup)
#printf "Result of workspace create:\n $ws_result \n"
#
## Generate service principal credentials
#printf "${grn}GENERATE SERVICE PRINCIPAL CREDENTIALS...${end}\n"
#credentials=$(az ad sp create-for-rbac --name "sp$resourcegroup" \
#	--scopes /subscriptions/$sub_id/resourcegroups/$resourcegroup \
#	--role Contributor \
#	--sdk-auth)
#
## Create config_file in specific format
#printf "${grn}WRITING OUT CONFIG_FILE VARIABLES...${end}\n"
#configFile='config.json'
#printf "{\n" > $configFile
#printf "\t \"subscription_id\":\"$sub_id\", \n">> $configFile
#printf "\t \"resource_group\":\"$resourcegroup\", \n">> $configFile
#printf "\t \"workspace_name\":\"$workspacename\" \n">> $configFile
#printf "}\n" >> $configFile
#
## Capture credentials for 'jq' parsing
#sleep 5
#credFile='cred.json'
#printf "$credentials" > $credFile
#clientID=$(cat $credFile | jq '.clientId')
#clientSecret=$(cat $credFile | jq '.clientSecret')
#tenantID=$(cat $credFile | jq '.tenantId')
#rm $credFile
#
## Create variables file
#printf "${grn}WRITING OUT SERVICE PRINCIPAL VARIABLES...${end}\n"
#env_variable_file='variables.env'
#printf "CLIENT_ID=$clientID \n" > $env_variable_file
#printf "CLIENT_SECRET=$clientSecret \n" >> $env_variable_file
#printf "TENANT_ID=$tenantID \n" >> $env_variable_file
#printf "SUB_ID=$sub_id \n" >> $env_variable_file
#printf "RESOURCE_GROUP=$resourcegroup \n" >> $env_variable_file
#printf "WORKSPACE_NAME=$workspacename \n" >> $env_variable_file
#
## Allow some time for operations to settle in the system
#printf "${grn}GRAB A COFFEE FOR 1 MINUTE......${end}\n"
#sleep 60
