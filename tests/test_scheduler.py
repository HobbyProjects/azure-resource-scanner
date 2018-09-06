from Adapters.Simulators import ServiceFactorySimulator
from Common.Test import TestCase
from Common import scheduler

from ast import literal_eval

class TestScheduler(TestCase):

    def read_config(self):
        self._simulated_factory = ServiceFactorySimulator()
        blob_service = self._simulated_factory.config_container()

        result = scheduler.read_config_from_blob(blob_service)
        return result

    def test_latest_config_is_picked(self):

        result = self.read_config()
        self.assertFalse(result is None)

        subscriptions = result['subscriptions']
        for subscription in subscriptions:
            self.assertFalse(subscription is None)

    def test_tasks_are_created(self):

        result = self.read_config()
        tasks = scheduler.create_tasks(result)
        for task in tasks:
            task_dict = literal_eval(task)
            id = task_dict['subscriptionId']
            type = task_dict['typeName']
            self.assertFalse(id is None)
            self.assertFalse(type is None)

    def test_push_tasks_to_queue(self):

        result = self.read_config()
        tasks = scheduler.create_tasks(result)

        queue_name = 'simulated_queue'
        task_queue = self._simulated_factory.queue(queue_name)
        scheduler.push_tasks_to_queue(task_queue, tasks)

        for task in tasks:
            task_dict = literal_eval(task)
            task_in_queue_dict =literal_eval(task_queue.pop())
            self.assertTrue(task_dict['subscriptionId'] == task_in_queue_dict['subscriptionId'])
            self.assertTrue(task_dict['typeName'] == task_in_queue_dict['typeName'])


