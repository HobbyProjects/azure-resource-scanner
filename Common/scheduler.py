import json
import logging


def create_tasks(config):

    tasks = []
    # put the tasks in the queue
    for subscription in config['subscriptions']:
        # handle the scenario where no resource type is specified
        if config['resourceTypes'] is None:
            sub_id = subscription['subscriptionId']

            data = {
                'subscriptionId': sub_id
            }
            message = json.dumps(data)
            tasks.append(message)

        for resource_type in config['resourceTypes']:
            sub_id = subscription['subscriptionId']
            r_type = resource_type['typeName']

            data = {
                'subscriptionId': sub_id,
                'typeName': r_type
            }
            message = json.dumps(data)
            tasks.append(message)

    return tasks


def read_config_from_blob(blob_service):

    # get a list of files in the blob container
    config_list = blob_service.list_blobs()

    # find the most recent config file
    latest_config = "config-"
    for config_filename in config_list:

        if config_filename.name > latest_config:
            latest_config = config_filename.name

    if latest_config == "config-":
        logging.error("Could not find any config files in blob container")
        return None

    # read the contents of the latest config
    json_data = blob_service.get_blob_to_text(latest_config).content
    if json_data == '{}':
        logging.error("Empty JSON returned!")
        return None
    return json.loads(json_data)


def push_tasks_to_queue(task_queue, tasks):

    for task in tasks:
        logging.info(f"Pushing task {task} to task queue")
        task_queue.push(task)
