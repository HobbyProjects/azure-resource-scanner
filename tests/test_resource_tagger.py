from Adapters.Simulators import ServiceFactorySimulator
from Common import ResourceTagger
from Common.Test import TestCase


class ResourceScannerTest(TestCase):

    def _get_factory(self):
        return ServiceFactorySimulator()

    def test_scanner_multiple_write(self):
        target_tags = {
            'tag1': 'value',
            'tag2': 'value'
        }

        factory = self._get_factory()
        resource_service = factory.resource_service(None)
        resource_tagger = ResourceTagger(factory, target_tags, True)

        resource = resource_service.get_resources()[0]

        tags_written, tags_skipped = resource_tagger.execute(resource)

        assert(tags_written == 2)
        assert(tags_skipped == 0)

    def test_scanner_overwrite(self):
        test_tag_name = 'testTag1'
        test_tag_value = 'testTag1Value'
        test_tag_default_value = 'default'

        target_tags = dict()
        target_tags[test_tag_name] = test_tag_value

        factory = self._get_factory()
        resource_service = factory.resource_service(None)
        resource_tagger = ResourceTagger(factory, target_tags, True)

        resource = resource_service.get_resources()[0]

        ### Test does overwrite

        resource.tags = target_tags.copy()
        resource.tags[test_tag_name] = test_tag_default_value

        tags_written, tags_skipped = resource_tagger.execute(resource)

        assert(tags_written == 1)
        assert(tags_skipped == 0)
        assert(resource.tags[test_tag_name] == test_tag_value)

        ### Test does not overwrite

        resource.tags = target_tags.copy()
        resource.tags[test_tag_name] = test_tag_default_value

        tags_written, tags_skipped = resource_tagger.execute(resource, False)

        assert(tags_written == 0)
        assert(tags_skipped == 1)
        assert(resource.tags[test_tag_name] == test_tag_default_value)
