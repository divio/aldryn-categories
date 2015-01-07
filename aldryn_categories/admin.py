# -*- coding: utf-8 -*-

from django.contrib import admin

from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category


class CategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ('name', 'slug')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
            ),
        }),
    )


admin.site.register(Category, CategoryAdmin)
