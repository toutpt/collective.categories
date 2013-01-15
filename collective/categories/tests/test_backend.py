import unittest2 as unittest
from collective.categories.tests import base
from collective.categories import backend
from collective.categories.backend import DefaultBackend, DefaultExtender
from collective.categories.backend_linguakeyword import Backend as LKBackend
from collective.categories.backend_atvm import Backend as ATVMBackend

LK_BACKEND = 'archetypes.linguakeywordwidget'
ATVM_BACKEND = 'Products.ATVocabularyManager'


class TestBackend(base.IntegrationTestCase):
    """We tests the setup (install) of the addons. You should check all
    stuff in profile are well activated (browserlayer, js, content types, ...)
    """

    def test_schemaextender(self):
        self.setRole('Manager')
        field = self.document.getField('categories')
        self.assertTrue(field is not None)

    def test_get_backend(self):
        self.setCategories(self.document, ['categorie 1'])
        backend_d = backend.get_backend(self.document)
        self.assertIsInstance(backend_d, DefaultBackend)
        registry = self.portal.portal_registry

        registry['collective.categories.backend'] = LK_BACKEND
        backend_lk = backend.get_backend(self.document)
        self.assertIsInstance(backend_lk, LKBackend)

        registry['collective.categories.backend'] = ATVM_BACKEND
        backend_atvm = backend.get_backend(self.document)
        self.assertIsInstance(backend_atvm, ATVMBackend)

        registry['collective.categories.backend'] = 'default'

    def test_default_backend(self):
        self.setCategories(self.document, ['categorie 1'])
        res = backend.get_backend(self.document)
        categories = res.get_categories()
        indexer = res.indexer()
        #check there is only one categorie
        self.assertEqual(len(categories), 1)
        self.assertEqual(len(indexer), 1)
        self.assertEqual(indexer[0], categories[0][0])
        #default backend as same key/value pairs
        self.assertEqual(categories[0][0], categories[0][1])
        #check the extender class
        self.assertEqual(res.get_extender_class(), DefaultExtender)

    def test_lkbackend(self):
        registry = self.portal.portal_registry
        registry['collective.categories.backend'] = LK_BACKEND
        backend_lk = backend.get_backend(self.document)
        self.document.setLanguage('fr')
        self.setCategories(self.document, ['fr-categorie 1'])
        indexer = backend_lk.indexer()
        categories = backend_lk.get_categories()
        self.assertNotEqual(categories[0][0], categories[0][1])
        self.assertEqual(indexer[0], categories[0][0])
        self.assertEqual(categories[0][0], 'fr-categorie 1')
        self.assertEqual(categories[0][1], 'categorie 1')

    def test_atvmbackend(self):
        registry = self.portal.portal_registry
        registry['collective.categories.backend'] = ATVM_BACKEND
        backend_atvm = backend.get_backend(self.document)
        #FIXME: check the base setup


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
