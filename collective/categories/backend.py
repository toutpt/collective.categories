from zope import interface, i18nmessageid
from zope import component
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.interfaces.base import IBaseContent

_ = i18nmessageid.MessageFactory('collective.categories')


class ICategoriesBackend(interface.Interface):
    """Categorie backend provide the necessary to store and index categories"""

    def indexer():
        """Use the context to retrive values
        -> [encoded string categorie, ...]
        """

    def get_extender_class():
        """Return the class to use as extender"""


class ExtensionCategoriesField(ExtensionField, atapi.LinesField):
    """ Retrofitted date field """


class DefaultExtender(object):
    """default extender use keyword"""

    fields = [
        ExtensionCategoriesField("categories",
            schemata="categorization",
            widget=atapi.KeywordWidget(label=_(u"Categories")),
            )
    ]

    def __init__(self, context):
        self.context = context


class DefaultBackend(object):
    """This is the default backend"""
    interface.implements(ICategoriesBackend)
    component.adapts(IBaseContent)

    def __init__(self, context):
        self.context = context

    def get_extender_class(self):
        return DefaultExtender

    def default_indexer(self):
        field = self.context.getField('categories')
        if not field:
            return
        values = field.get(self.context)
        return values
