import types
from Products.CMFCore.utils import getToolByName
#from Products.ATVocabularyManager.utils.vocabs import fetchValueByKeyFromVocabularyDict


def getPathFromVDict(searchedkey, vdict, path=""):
    """recursive find of a key in the vocabulary dictionary tree."""

    for key in vdict.keys():
        newpath = path + '/' + key
        if key == searchedkey:
            return newpath

        elif vdict[key] not in types.StringTypes:
            if not vdict[key][1]:
                continue
            rpath = getPathFromVDict(searchedkey,
                                     vdict[key][1],
                                     path=newpath)
            if rpath is not None:
                return rpath

    return None


def indexer(context):
    categories = []

    field = context.getField('categories')
    if not field:
        return
    values = field.get(context)
    if not values:
        return
    atvm = getToolByName(context, 'portal_vocabularies')
    if not atvm:
        return
    vocab = atvm.getVocabularyByName('collective_categories')
    if not vocab:
        return
    vdict = vocab.getVocabularyDict()

    for uid in values:
        path = getPathFromVDict(uid, vdict)

        if path:
            cdict = vdict
            for key in path.split('/'):
                if key:
                    categories.append(cdict[key][0])
                    cdict = cdict[key][1]

    return categories
