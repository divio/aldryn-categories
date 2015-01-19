# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError, models
from django.template.defaultfilters import slugify as default_slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager, TranslatableQuerySet

from treebeard.ns_tree import NS_Node, NS_NodeManager, NS_NodeQuerySet


if settings.LANGUAGES:
    LANGUAGE_CODES = [language[0] for language in settings.LANGUAGES]
elif settings.LANGUAGE:
    LANGUAGE_CODES = [settings.LANGUAGE]
else:
    raise ImproperlyConfigured(
        'Neither LANGUAGES nor LANGUAGE was found in settings.')


class CategoryQuerySet(TranslatableQuerySet, NS_NodeQuerySet):
    pass


class CategoryManager(TranslatableManager, NS_NodeManager):
    queryset_class = CategoryQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db
        ).order_by('tree_id', 'lft')

    if django.VERSION < (1, 8):
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
class Category(TranslatableModel, NS_Node):
    """
    A category is hierarchical. The structure is implemented with django-
    treebeard's Nested Sets trees, which has the performance characteristics
    we're after, namely: fast reads at the expense of write-speed.
    """

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

    def slugify(self, category, i=None):
        slug = default_slugify(category)
        if i is not None:
            slug += "_%d" % i
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.name)
            try:
                return super(Category, self).save(*args, **kwargs)
            except IntegrityError:
                pass

            for lang in LANGUAGE_CODES:
                #
                # We'd much rather just do something like:
                #     Category.objects.translated(lang,
                #         slug__startswith=self.slug)
                # But sadly, this isn't supported by Parler/Django, see:
                #     http://django-parler.readthedocs.org/en/latest/api/\
                #         parler.managers.html#the-translatablequeryset-class
                #
                slugs = []
                all_slugs = Category.objects.language(lang).exclude(
                    id=self.id).values_list('translations__slug', flat=True)
                for slug in all_slugs:
                    if slug and slug.startswith(self.slug):
                        slugs.append(slug)
                i = 1
                while True:
                    slug = self.slugify(self.name, i)
                    if slug not in slugs:
                        self.slug = slug
                        return super(Category, self).save(*args, **kwargs)
                    i += 1
        else:
            return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)
