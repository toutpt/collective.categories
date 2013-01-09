from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs


def importVarious(self):

    if self.readDataFile('collective.categories.txt') is None:
        return

    site = self.getSite()
    atvm = getToolByName(site, 'portal_vocabularies')
    vkey = 'collective_categories'
    vocab = atvm.getVocabularyByName(vkey)

    if not vocab:
        vdict = {(vkey, 'collective.categories'): {}}
        createHierarchicalVocabs(atvm, vdict)
        vocab = atvm.getVocabularyByName(vkey)
