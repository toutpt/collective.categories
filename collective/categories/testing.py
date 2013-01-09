from plone.testing import z2

from plone.app.testing import *
import collective.categories

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.categories,
                                additional_z2_products=[],
                                gs_profile_id='collective.categories:default',
                                name="collective.categories:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.categories:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.categories:Functional")

