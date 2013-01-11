from plone.indexer import indexer
from Products.Archetypes.interfaces.base import IBaseObject
from zope.component import getUtility, queryAdapter
from plone.registry.interfaces import IRegistry
from collective.categories.backend import ICategoriesBackend, DefaultBackend


@indexer(IBaseObject)
def categories(context):
    registry = getUtility(IRegistry)
    name = registry.get('collective.categories.backend', 'default')
    backend = queryAdapter((context, ),
                         interface=ICategoriesBackend,
                         name=name)
    if not backend:
        backend = DefaultBackend(context)
    return backend.indexer()
