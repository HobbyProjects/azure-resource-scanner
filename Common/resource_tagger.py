import logging
from Common.Contracts import ServiceFactory
from .Contracts import Resource


class ResourceTagger:
    def __init__(self, factory: ServiceFactory, tags:dict, overwrite=True):
        self._factory = factory
        self._tags = tags
        self._overwrite = overwrite

    def execute(self, resource: Resource, overwrite=None):

        # Default overwrite behavior
        if overwrite is None:
            overwrite = self._overwrite

        # Tag the resource
        tags_written = 0
        tags_skipped = 0
        for tag_key, tag_value in self._tags.items():
            if not overwrite and tag_key in resource.tags:
                logging.info(f"Skipped tagging {resource.id} with tag {tag_key} since it already exists.")
                tags_skipped += 1
                continue
            resource.tags[tag_key] = tag_value
            tags_written += 1

        # Only save if needed
        if tags_written > 0:
            self._factory.resource_service(resource.account_id).update_resource(resource)
            logging.info(f"Wrote {tags_written} tags to {resource.id}.")

        return tags_written, tags_skipped
