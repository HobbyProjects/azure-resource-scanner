# Azure Resource Scanner
Workflow for discovering and documenting Azure Resources across multiple subscriptions with the intent to store, update tags, and/or perform other generic resource related operations.

Logic is written in Python and is executed by Azure Functions.

[![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fericmaino%2Fazure-resource-scanner%2Fmaster%2FDeployment%2Fdeploy.azure.json)
[![Visualize](http://armviz.io/visualizebutton.png)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2Fericmaino%2Fazure-resource-scanner%2Fmaster%2FDeployment%2Fdeploy.azure.json)

#### Setup Azure for Deployment

Using the Azure CLI, either from inside the Azure Portal using Cloud Shell, or locally. [Download Local CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)

It is recommended you do this using the Azure Portal Cloud Shell, in PowerShell Mode ,if you are not using Cloud Shell then you must first sign in using ```az login```

*Note: If you have more than one subscription you can select which to use with```az account set --subscription ```*

##### 1. Create Resource Group
All resources must belong to a storage account:

```az group create --name my-functions-group --location westus2```

##### 2. Create Storage Account
This storage account is used by the Azure Function. In the following command, substitute a globally unique storage
account name where you see the ```<storage-name>``` placeholder. The name must be between 3 and 24 characters
and may only contain lowercase letters and numbers.

```az storage account create --name <storage-name> --location westus2 --resource-group my-functions-group --sku Standard_LRS```


##### 3. Create Linux App Service plan
Running the functions via docker container requires a Linux App Service.

```
az appservice plan create --name my-app-service --resource-group my-functions-group --sku S1 --is-linux
```

##### 4. Create the Azure Function and deploy the image
The function app executes the functions inside of the docker image.

In the following command, substitute a unique function app name where you see the <app_name> placeholder 
and the storage account name for ```<storage_name>```. The ```<app_name>``` is used as the default DNS 
domain for the function app, and so the name needs to be unique across all apps in Azure. 
As before, ```<docker-id>``` is your Docker account name.

```
az functionapp create --name <app_name> --storage-account  <storage_name>  --resource-group my-functions-group --plan my-app-service --deployment-container-image-name <docker-id>/my-functions:v1
```

##### 5. Configure the storage accounts for the function app
The function app requires connection strings to connect to the Storage Account created earlier.

```
storageConnectionString=$(az storage account show-connection-string --resource-group my-functions-group --name <storage_account> --query connectionString --output tsv)

az functionapp config appsettings set --name <function_app> --resource-group my-functions-group --settings AzureWebJobsDashboard=$storageConnectionString AzureWebJobsStorage=$storageConnectionString
```

##### 6. Create an SPN to search Azure with
We use a service principal name (SPN) to perform Azure calls inside of the Azure Function. SPN's have no 
privileges by default and must be granted them for each subscription, resource group, or resource you 
wish for them to have access to.

To create the SPN, run the following command.
```
az ad sp create-for-rbac --name <spn-name> --password <spn-password>
```   
This should return something like this:
```
{
    "appId": <app-id>,
    "displayName": <spn-name>,
    "name": "http://<spn-name>",
    "password": <spn-password>,
    "tenant": <spn-tenant>
}
```
This has also created a `Contributor` role assignment for the service principal in the current subscription. To remove that role assignment and assign the principal a `Reader` role instead:

```bash
az role assignment create --assignee <app-id> --role Reader
# Only need to delete Contributor access for account previously set in CLI
az role assignment delete --assignee <app-id> --role Contributor
```

If you would like the Service Principal to have access to multiple subscriptions, perform the following commands with each subscription ID:

```bash
az account set --subscription <subscription-id>
az role assignment create --assignee <app-id> --role Reader
```

Roles can also be added/removed from inside the Azure Portal from the `Access Control (IAM)`
menu on any subscription, resource group, or resource.

##### 7. Add SPN login details to function app
We can allow the function app to login as the SPN by giving it the name, password, and tenant.
A secure way of doing this is adding these properties to the application settings for the function app.
This will allow the function app to access the properties as environment variables on runtime.

This command will add the SPN login details to the application settings:
```
az functionapp config appsettings set --name <function_app> --resource-group my-functions-group --settings ClientId=<app-id> ClientSecret=<spn-password> ClientTenant=<spn-tenant>
```

##### 8. Verify Function Configuration
The function app should now be configured properly. You can verify the functions are loaded correctly by finding them in the Azure Portal and opening the function app resource. In order for the flow to begin, there must be a configuration file, which is explained below.

##### 9. Generate Configuration File
In order for the Resource Scanner to run, a configuration file must be generated. This configuration file is stored in an Azure Blob Storage container, and then picked up by the task scheduling function to kick off the process. This process is run locally. Follow [these steps](/GenerateConfig.md) to generate the file, at which point you should be good to start scanning :)
