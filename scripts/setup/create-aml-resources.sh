#!/bin/bash
#Script to provision a new Azure ML workspace
grn=$'\e[1;32m'
end=$'\e[0m'

set -e

# Start of script
SECONDS=0
printf "${grn}STARTING CREATION OF WORKSPACE...${end}\n"

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription 
az account set -s $sub_id

# Source unique name for RG, workspace creation
unique_name='mlops_primer'
number=$[ ( $RANDOM % 10000 ) + 1 ]
resourcegroup=$unique_name$number
workspacename=$unique_name$number'workspace'
location='westus'

# Create a resource group
printf "${grn}STARTING CREATION OF RESOURCE GROUP...${end}\n"
rg_create=$(az group create \
	--name $resourcegroup \
	--location $location \
--only-show-errors)
#printf "Result of resource group create:\n $rg_create \n"

# Create workspace through CLI
printf "${grn}STARTING CREATION OF AML WORKSPACE...${end}\n"
ws_result=$(az ml workspace create \
	-n $workspacename \
	-g $resourcegroup \
--only-show-errors)
#printf "Result of workspace create:\n $ws_result \n"

# Generate service principal credentials
printf "${grn}GENERATE SERVICE PRINCIPAL CREDENTIALS...${end}\n"
credentials=$(az ad sp create-for-rbac --name "sp$resourcegroup" \
	--scopes /subscriptions/$sub_id/resourcegroups/$resourcegroup \
	--role Contributor \
	--sdk-auth \
--only-show-errors)

## Create config_file in specific format
#printf "${grn}WRITING OUT CONFIG_FILE VARIABLES...${end}\n"
#configFile='config.json'
#printf "{\n" > $configFile
#printf "\t \"subscription_id\":\"$sub_id\", \n">> $configFile
#printf "\t \"resource_group\":\"$resourcegroup\", \n">> $configFile
#printf "\t \"workspace_name\":\"$workspacename\" \n">> $configFile
#printf "}\n" >> $configFile

# Capture credentials for 'jq' parsing
sleep 5
credFile='cred.json'
printf "$credentials" > $credFile
clientID=$(cat $credFile | jq '.clientId')
clientSecret=$(cat $credFile | jq '.clientSecret')
tenantID=$(cat $credFile | jq '.tenantId')
rm $credFile

# Create variables file
printf "${grn}WRITING OUT SERVICE PRINCIPAL VARIABLES...${end}\n"
env_variable_file='variables.env'
printf "CLIENT_ID=$clientID \n" > $env_variable_file
printf "CLIENT_SECRET=$clientSecret \n" >> $env_variable_file
printf "TENANT_ID=$tenantID \n" >> $env_variable_file
printf "SUB_ID=$sub_id \n" >> $env_variable_file
printf "RESOURCE_GROUP=$resourcegroup \n" >> $env_variable_file
printf "WORKSPACE_NAME=$workspacename \n" >> $env_variable_file

# Allow some time for operations to settle in the system
printf "${grn}GRAB A COFFEE FOR 1 MINUTE......${end}\n"
sleep 60
