from zope.component import adapts
from zope.interface import implements

from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, \
    IBrowserLayerAwareExtender

from collective.categories.layer import Layer
from Products.ATVocabularyManager import NamedVocabulary
from zope import i18nmessageid
_ = i18nmessageid.MessageFactory('collective.categories')


class ExtensionCategoriesField(ExtensionField, atapi.LinesField):
    """ Retrofitted date field """


class CategoriesExtender(object):
    """Add Categories field"""

    adapts(IBaseContent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = Layer

    fields = [
        ExtensionCategoriesField("categories",
            schemata="categorization",
            vocabulary=NamedVocabulary('collective_categories'),
            widget=atapi.MultiSelectionWidget(label=_(u"Categories")),
            )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """getOrder
        """
        schematas["categorization"].append('categories')

        return schematas

    def getFields(self):
        """getFields
        """
        return self.fields
