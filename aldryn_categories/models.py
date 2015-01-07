# -*- coding: utf-8 -*-

from django.db import IntegrityError, models
from django.template.defaultfilters import slugify as default_slugify

from treebeard.ns_tree import NS_Node


class CategoryBase(NS_Node):
    """
    A category is just a hierarchical tag. The structure is implemented with
    django-treebeard's Nested Sets trees, which has the performance
    characteristics we're after, namely: fast reads at the expense of write-
    speed.
    """

    node_order_by = ['name', ]

    name = models.CharField(
        blank=False,
        default='',
        max_length=255
    )

    slug = models.SlugField(
        max_length=255
    )

    class Meta:
        abstract = True

    def slugify(self, category, i=None):
        slug = default_slugify(category)
        if i is not None:
            slug += "_%d" % i
        return slug

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            try:
                return super(CategoryBase, self).save(self, *args, **kwargs)
            except IntegrityError:
                pass

            # Find similar slugs
            slugs = set(Category.objects
                                .filter(slug__startswith=self.slug)
                                .values_list('slug', flat=True))
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    return super(CategoryBase, self).save(self, *args, **kwargs)
                i += 1
        else:
            return super(CategoryBase, self).save(self, *args, **kwargs)


class Category(CategoryBase):
    """
    A thin but concrete implementation of CategoryBase.
    """
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
