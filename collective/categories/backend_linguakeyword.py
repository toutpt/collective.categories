from zope import component
from zope import i18nmessageid
from zope import interface
from Products.Archetypes import atapi

from archetypes.schemaextender.field import ExtensionField
from archetypes.linguakeywordwidget import LinguaKeywordWidget

from collective.categories import backend
from Products.Archetypes.interfaces.base import IBaseContent

_ = i18nmessageid.MessageFactory('collective.categories')


class ExtensionCategoriesField(ExtensionField, atapi.LinesField):
    """ Retrofitted date field """


class CategoriesExtender(object):
    """Add Categories field"""

    fields = [
        ExtensionCategoriesField("categories",
            schemata="categorization",
            widget=LinguaKeywordWidget(label=_(u"Categories")),
            )
    ]

    def __init__(self, context):
        self.context = context


class Backend(object):
    interface.implements(backend.ICategoriesBackend)
    component.adapts(IBaseContent)

    def __init__(self, context):
        self.context = context

    def indexer(self):
        field = self.context.getField('categories')
        if not field:
            return

        values = field.get(self.context)
        return values

    def get_extender_class(self):
        """Return the class to use as extender"""
        return CategoriesExtender
