from zope.component import adapts, getUtility, queryAdapter
from zope.interface import implements
from zope import i18nmessageid

from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces  import IBrowserLayerAwareExtender
from Products.Archetypes.interfaces import IBaseContent

from plone.registry.interfaces import IRegistry

from collective.categories.layer import Layer
from collective.categories.backend import ICategoriesBackend, DefaultBackend

_ = i18nmessageid.MessageFactory('collective.categories')


class CategoriesExtender(object):
    """Add Categories field"""

    adapts(IBaseContent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = Layer

    def __init__(self, context):
        self.context = context
        self.registry = None
        self.extender = None

    @property
    def fields(self):
        self.update()
        return self.extender.fields

    def getOrder(self, schematas):
        """getOrder
        """
        schematas["categorization"].append('categories')

        return schematas

    def getFields(self):
        """getFields
        """
        return self.fields

    def update(self):
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.extender is None:
            name = self.registry.get('collective.categories.backend',
                                     'default')
            backend = queryAdapter((self.context, ),
                                 interface=ICategoriesBackend,
                                 name=name)
            if not backend:
                backend = DefaultBackend(self.context)
            self.extender = backend.get_extender_class()(self.context)
