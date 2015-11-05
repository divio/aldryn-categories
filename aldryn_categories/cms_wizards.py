# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard
from cms.wizards.forms import BaseFormMixin

from parler.forms import TranslatableModelForm
from treebeard.forms import movenodeform_factory, MoveNodeForm

from .models import Category


class CategoryWizard(Wizard):

    def get_success_url(self, *args, **kwargs):
        # get category object and if it has page return it's url,
        # otherwise redirect to root.
        obj = kwargs['obj']
        if hasattr(obj, 'page'):
            return obj.page.get_absolute_url(kwargs['language'])
        return '/'


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