# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from aldryn_translation_tools.models import (
    TranslatedAutoSlugifyMixin, TranslationHelperMixin)
from parler import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields
from treebeard.ns_tree import NS_Node, NS_NodeManager, NS_NodeQuerySet

LANGUAGE_CODES = appsettings.PARLER_LANGUAGES.get_active_choices()


class CategoryQuerySet(TranslatableQuerySet, NS_NodeQuerySet):
    pass


class CategoryManager(TranslatableManager, NS_NodeManager):
    queryset_class = CategoryQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db
        ).order_by('tree_id', 'lft')

    if django.VERSION < (1, 8):  # pragma: no cover
        get_query_set = get_queryset


#
# TODO: I would have preferred to make this a base class "CategoryBase" which
# is Abstract, then subclass it as a concrete Category class. But, Parler
# cannot be applied to an Abstract class.
#
# TODO: At some point, consider an approach like this:
#     https://gist.github.com/GaretJax/7c7a9acc055c05c65041
#
@python_2_unicode_compatible
class Category(TranslatedAutoSlugifyMixin, TranslationHelperMixin,
               TranslatableModel, NS_Node):
    """
    A category is hierarchical. The structure is implemented with django-
    treebeard's Nested Sets trees, which has the performance characteristics
    we're after, namely: fast reads at the expense of write-speed.
    """
    slug_source_field_name = 'name'

    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            blank=False,
            default='',
            max_length=255,
        ),
        slug=models.SlugField(
            _('slug'),
            blank=True,
            default='',
            help_text=_('Provide a “slug” or leave blank for an automatically '
                        'generated one.'),
            max_length=255,
        ),
        meta={'unique_together': (('language_code', 'slug', ), )}
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    objects = CategoryManager()

    def delete(self, using=None):
        #
        # We're simply managing how the two superclasses perform deletion
        # together here.
        #
        self.__class__.objects.filter(pk=self.pk).delete(using)
        super(TranslatableModel, self).delete()

    def __str__(self):
        name = self.safe_translation_getter('name', any_language=True)
        return escape(name)
