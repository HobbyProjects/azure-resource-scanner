from Common.Contracts import Resource
from Common.Helpers import ResourceExtractors
from json import dumps


class AzureResource(Resource):

    def __init__(self, d: dict):
        resource_id = d['id']
        self.subscription_id = ResourceExtractors.get_subscription(resource_id)
        self.resource_group = ResourceExtractors.get_resource_group(resource_id)
        self.resource_name = d['name']
        self.resource_type = d['type']
        self.resource_location = d['location']
        self.resource_tags = d.get('tags', {})

    @property
    def id(self):
        return f"/subscriptions/{self.account_id}/resourceGroups/" \
               f"{self.resource_group}/providers/{self.type}/{self.name}"

    @property
    def account_id(self):
        return self.subscription_id

    @property
    def name(self):
        return self.resource_name

    @property
    def type(self):
        return self.resource_type

    @property
    def location(self):
        return self.resource_location

    @property
    def tags(self):
        return self.resource_tags

    @tags.setter
    def tags(self, tags):
        self.resource_tags = tags

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'tags': self.tags
        }

    def to_str(self):
        return dumps(self.to_dict())
