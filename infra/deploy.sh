#/bin/bash
if [ -z "$2" ]
  then
    echo "Invalid parameters - Usage: deploy.sh <project-name> <region>"
    exit 1
fi
project_name=$1
region=$2

echo "Creating the 'AI Developers' group..."
group_id=$(az ad group create --display-name "AI Developers" --mail-nickname "AIDevelopers" --output tsv --query id)

echo "Deploying project $project_name to Azure..."
outputs=$(az deployment sub create \
  --name "${project_name}_deployment" \
  --location $region \
  --template-file infra/main.bicep \
  --parameters projectName=$project_name aiDevelopersGroupPrincipalId=$group_id \
  --output tsv \
  --query "[properties.outputs.openAiEndpoint.value, properties.outputs.dbConnectionString.value]"
)
echo "Project $project_name deployed successfully."

echo "Creating an .env file in app/.env ..."
openai_endpoint=$(echo $outputs | cut -d' ' -f1)
db_connection_string=$(echo $outputs | cut -d' ' -f2)

echo -e "OPENAI_ENDPOINT=$openai_endpoint\nAZURE_SQL_CONNECTIONSTRING=Driver={ODBC Driver 18 for SQL Server};$db_connection_string" > 'app/.env'