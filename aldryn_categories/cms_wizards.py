# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib.parse import urlunparse  # Py3
except ImportError:
    from urlparse import urlunparse  # Py2

from django.utils.translation import ugettext_lazy as _
from django.utils.six.moves.urllib.parse import urlparse as six_urlparse

from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard
from cms.wizards.forms import BaseFormMixin
from cms.utils import get_cms_setting

from parler.forms import TranslatableModelForm
from treebeard.forms import movenodeform_factory, MoveNodeForm

from .models import Category


class CategoryWizard(Wizard):

    def get_success_url(self, *args, **kwargs):
        # get category object and if it has page return it's url,
        # otherwise redirect to root.
        obj = kwargs['obj']
        if hasattr(obj, 'page'):
            url = obj.page.get_absolute_url(kwargs.get('language'))
        else:
            url = '/'
        # Add 'edit' to GET params of URL
        if self.edit_mode_on_success:
            (scheme, netloc, path, params, query, fragment) = six_urlparse(url)
            query = get_cms_setting('CMS_TOOLBAR_URL__EDIT_ON')
            url = urlunparse((scheme, netloc, path, params, query, fragment))
        return url


class CreateCategoryForm(BaseFormMixin, TranslatableModelForm, MoveNodeForm):
    """
    The model form for Category wizad.
    """

    def save(self, *args, **kwargs):
        # since original page is not accessible in Wizard.get_success_url
        # here is a little hack to track original page. please fix if possible
        obj = super(CreateCategoryForm, self).save(*args, **kwargs)
        if self.page:
            setattr(obj, 'page', self.page)
        return obj

    class Meta:
        model = Category
        fields = ['name', 'slug', ]


aldryn_category_wizard = CategoryWizard(
    title=_(u"New category"),
    weight=290,
    form=movenodeform_factory(Category, form=CreateCategoryForm),
    description=_(u"Create a new category.")
)

wizard_pool.register(aldryn_category_wizard)
