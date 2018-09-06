import click
from Adapters.Azure import AzureServiceFactory
from Adapters.Azure.Config import AzureConfig
from Common import Config


@click.command()
@click.option('-t', '--types', type=click.STRING, required=True,
              help="Resource types for which to scan in Azure subscriptions, separated by comma")
def generate_config_cli(types):
    type_list = types.split(',')
    azure_config = AzureConfig(Config())
    azure_factory = AzureServiceFactory(azure_config)
    generator = azure_factory.config_generator()
    container = azure_factory.config_container()
    generator.execute(type_list, container)


if __name__ == '__main__':
    generate_config_cli()  # pylint: disable=E1120
