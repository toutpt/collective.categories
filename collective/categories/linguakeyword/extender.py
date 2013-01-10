from Products.Archetypes import atapi

from archetypes.schemaextender.field import ExtensionField
from archetypes.linguakeywordwidget import LinguaKeywordWidget

from zope import i18nmessageid
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
