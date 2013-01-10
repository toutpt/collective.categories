import types
import pkg_resources
from plone.indexer import indexer
from Products.Archetypes.interfaces.base import IBaseObject
from Products.CMFCore.utils import getToolByName
from zope.component._api import getUtility
from plone.registry.interfaces import IRegistry

try:
    pkg_resources.get_distribution('Products.ATVocabularyManager')
    from collective.categories.atvm import indexer as atvm_indexer
except pkg_resources.DistributionNotFound:
    pass
try:
    pkg_resources.get_distribution('archetypes.linguakeywordwidget')
    from collective.categories.linguakeyword import indexer as lk_indexer
except pkg_resources.DistributionNotFound:
    pass


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


def default_indexer(context):
    field = context.getField('categories')
    if not field:
        return
    values = field.get(context)
    return values


@indexer(IBaseObject)
def categories(context):
    registry = getUtility(IRegistry)
    name = registry.get('collective.categories.backend', 'default')
    if name == 'Products.ATVocabularyManager':
        return atvm_indexer.indexer(context)
    elif name == 'archetypes.linguakeywordwidget':
        return lk_indexer.indexer(context)
    return default_indexer(context)
