import transaction
import unittest2 as unittest
from plone.app import testing
from collective.categories import testing as ctesting
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs
from plone import api


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):

    layer = ctesting.INTEGRATION

    def login(self):
        testing.login(self.portal, testing.TEST_USER_NAME)

    def logout(self):
        testing.logout()

    def setRole(self, role):
        if role:
            testing.setRoles(self.portal, testing.TEST_USER_ID, [role])

    def setCategories(self, document, categories):
        document.getField('categories').set(document, categories)
        document.reindexObject()

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']

        self.login()
        self.setRole('Manager')
        self.document = api.content.create(type='Document',
                                          title='test document',
                                          container=self.portal)
        self.setRole('Member')

    def setUpATVM(self):
        #FIXME: raise Unauthorize on invokeFactory done by the create
        atvm = self.portal.portal_vocabularies
        vkey = 'collective_categories'
        vocab = atvm.getVocabularyByName(vkey)

        if not vocab:
            vdict = {(vkey, 'collective.categories'): {}}
            createHierarchicalVocabs(atvm, vdict)
            vocab = atvm.getVocabularyByName(vkey)


class FunctionalTestCase(IntegrationTestCase):

    layer = ctesting.FUNCTIONAL

    def setUp(self):
        #we must commit the transaction
        transaction.commit()
