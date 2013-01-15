import unittest2 as unittest
from collective.categories.tests import base


class TestSetup(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_create_and_index(self):
        self.setRole('Manager')
        self.setCategories(self.document, ['categorie 1'])
        self.document.reindexObject()
        catalog = self.portal.portal_catalog
        query = {'portal_type': 'Document',
                 'categories': 'categorie 1'}
        brains = catalog(**query)
        self.assertEquals(len(brains), 1)

    def test_portal_atct(self):
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
