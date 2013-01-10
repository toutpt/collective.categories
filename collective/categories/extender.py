import pkg_resources
from zope.component import adapts, getUtility
from zope.interface import implements
from zope import i18nmessageid

from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, \
    IBrowserLayerAwareExtender

from collective.categories.layer import Layer
from plone.registry.interfaces import IRegistry

try:
    pkg_resources.get_distribution('Products.ATVocabularyManager')
    from collective.categories.atvm import extender as atvm_extender
except pkg_resources.DistributionNotFound:
    pass
try:
    pkg_resources.get_distribution('archetypes.linguakeywordwidget')
    from collective.categories.linguakeyword import extender as lk_extender
except pkg_resources.DistributionNotFound:
    pass

_ = i18nmessageid.MessageFactory('collective.categories')


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
            if name == 'Products.ATVocabularyManager':
                self.extender = atvm_extender.CategoriesExtender(self.context)
            elif name == 'archetypes.linguakeywordwidget':
                self.extender = lk_extender.CategoriesExtender(self.context)
            else:
                self.extender = DefaultExtender(self.context)
