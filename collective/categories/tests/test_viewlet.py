import unittest2 as unittest
from collective.categories.tests import base
from collective.categories.viewlet import Categories


class IntegratTestViewlet(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_update(self):
        self.setRole('Manager')
        self.setCategories(self.document, ['categorie 1', 'categorie 2'])
        self.document.setSubject(['tag 1', 'tag 2'])
        self.document.reindexObject()
        viewlet = Categories(self.document, self.request, None)
        viewlet.update()
        self.assertTrue(hasattr(viewlet, 'categories'))
        self.assertEqual(len(viewlet.categories), 2)
        self.assertIn(('categorie 1', 'categorie 1'), viewlet.categories)
        self.assertIn(('categorie 2', 'categorie 2'), viewlet.categories)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
