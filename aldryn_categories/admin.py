# -*- coding: utf-8 -*-

import pdb

from django.contrib import admin

from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from .models import Category


class CategoryBaseForm(MoveNodeForm, TranslatableModelForm):
    pass


class CategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(Category, form=CategoryBaseForm)
    # list_display = ('name', 'slug', 'position', 'ref_node_id')
    # fieldsets = (
    #     (None, {
    #         'fields': (
    #             'name',
    #             'slug',
    #         ),
    #     }),
    # )

    # def clean(self, *args, **kwargs):
    #     pdb.set_trace()

admin.site.register(Category, CategoryAdmin)
