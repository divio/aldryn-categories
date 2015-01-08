# -*- coding: utf-8 -*-

from django.contrib import admin

from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from .models import Category


class CategoryForm(TranslatableModelForm, MoveNodeForm):
    pass


class CategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(Category, form=CategoryForm)

admin.site.register(Category, CategoryAdmin)
