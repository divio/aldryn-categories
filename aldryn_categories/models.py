# -*- coding: utf-8 -*-

from django.db import models
from taggit import models as taggit
from treebeard import ns_tree as treebeard


class CategoryBase(taggit.TagBase, treebeard.NS_Node):
    """
    A category is just a hierarchical tag. The structure is implemented with
    django-treebeard's Nested Sets trees, which has the performance
    characteristics we're after, namely: fast reads at the expense of write-
    speed.
    """

    node_order_by = ['name', ]

    class Meta:
        abstract = True

    # Treebeard requires this custom manager
    objects = treebeard.NS_NodeManager()


class Category(CategoryBase):
    """
    A thin but concrete implementation of CategoryBase.
    """
    pass


class CategorisedItemBase(taggit.ItemBase):

    category = models.ForeignKey(Category)

    class Meta:
        abstract = True

    @classmethod
    def category_model(cls):
        return cls._meta.get_field_by_name("category")[0].rel.to

    @classmethod
    def category_relname(cls):
        return cls._meta.get_field_by_name('category')[0].rel.related_name

    @classmethod
    def categories_for(cls, model, instance=None):
        if instance is not None:
            return cls.category_model().objects.filter(**{
                '%s__content_object' % cls.category_relname(): instance
            })
        return cls.cateogry_model().objects.filter(**{
            '%s__content_object__isnull' % cls.category_relname(): False
        }).distinct()


class CategorisedItem(taggit.GenericTaggedItemBase, CategorisedItemBase):
    pass
