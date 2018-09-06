# Generate a Config File

In order for the Resource Scanner to run, a configuration file must be generated. This configuration file is stored in an Azure Blob Storage container, and then picked up by the task scheduling function to kick off the process. This process is run locally.

To generate your config file, follow these steps:

1. Make sure you have [Python 3+](https://www.python.org/downloads/) and [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) installed

2. Clone this repository and `cd` into directory
    ```bash
    git clone <REPO-URL>
    cd azure-resource-scanner
    ```

3. Create your virtual environment
    ```bash
    virtualenv myenv
    ```

4. Activate the environment (using OS specific command)
    ```bash
    # Windows
    myenv/Scripts/activate

    # Linux/MacOS
    source myenv/bin/activate
    ```
5. Install all dependencies
    ```bash
    (myenv) pip install -r requirements.txt
    ```

6. Set appropriate environment variables (Note: this will set the environment variables only for your active shell session)
    
    **Windows** **(***For Linux/MacOS, use `export` instead of `set` below**)
    ```bash
    # See above for service principal details
    (myenv) set AZURE_CLIENT_ID=<app-id>
    (myenv) set AZURE_CLIENT_SECRET=<spn-password>
    (myenv) set AZURE_TENANT_ID=<spn-tenant>
    (myenv) set CONFIG_CONTAINER_BLOB=<name-of-blob-container-to-store-config>
    (myenv) set AzureWebJobsStorage=<azure-storage-account-connection-string>
    ```

7. Generate config
    ```bash
    (myenv) generate-config.py -t <RESOURCE-TYPE-1,RESOURCE-TYPE-2,...>
    # Example:
    # generate-config.py -t Microsoft.Compute/virtualMachines
    ```
    Click [here](/resource-types.md) for a full list of Azure resource types
