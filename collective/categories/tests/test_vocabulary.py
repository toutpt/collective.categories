import unittest2 as unittest
from zope import component
from collective.categories.tests import base
from zope.schema.interfaces import IVocabularyFactory


class UnitTestVocabulary(base.IntegrationTestCase):

    def test_categories_vocabulary(self):
        self.setRole('Manager')
        self.setCategories(self.document, ['categorie 1', 'categorie 2'])
        self.document.reindexObject()
        name = "collective.categories.vocabulary.categories"
        factory = component.queryUtility(IVocabularyFactory, name)
        vocab = factory(self.portal)
        self.assertEqual(len(vocab), 2)
        self.assertEqual(vocab.getTerm('categorie 1').title, u'categorie 1')
        self.assertEqual(vocab.getTerm('categorie 1').token, 'categorie 1')
        self.assertEqual(vocab.getTerm('categorie 1').value, 'categorie 1')

    def test_backend_vocabulary(self):
        name = "collective.categories.vocabulary.backends"
        factory = component.queryUtility(IVocabularyFactory, name)
        vocab = factory(self.document)
        self.assertEqual(len(vocab), 3)
        for name in ('default',
                     'Products.ATVocabularyManager',
                     'archetypes.linguakeywordwidget'):
            self.assertTrue(vocab.getTerm(name))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
