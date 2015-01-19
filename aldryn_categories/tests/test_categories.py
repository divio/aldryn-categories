# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, TransactionTestCase
from django.utils import translation
from parler.utils.context import switch_language

from aldryn_categories.models import Category
from aldryn_categories.fields import (
    CategoryMultipleChoiceField, CategoryManyToManyField)


class CategoryTestCaseMixin(object):
    """Mixin class for testing Categories"""

    @staticmethod
    def reload(node):
        """NOTE: django-treebeard requires nodes to be reloaded via the Django
        ORM once its sub-tree is modified for the API to work properly.

        See:: https://tabo.pe/projects/django-treebeard/docs/2.0/caveats.html

        This is a simple helper-method to do that."""
        return node.__class__.objects.get(id=node.id)


class TestCategories(CategoryTestCaseMixin, TransactionTestCase):
    """Implementation-specific tests"""

    def test_category_slug_creation(self):
        name = "Root Node"
        root = Category.add_root(name=name)
        root.set_current_language("en")
        root.save()
        self.assertEquals(root.slug, "root-node")

    def test_slug_collision(self):
        root = Category.add_root(name="test")
        root.save()
        root = self.reload(root)
        self.assertEquals(root.slug, "test")
        child1 = root.add_child(name="test")
        self.assertEquals(child1.slug, "test_1")
        child2 = root.add_child(name="test")
        self.assertEquals(child2.slug, "test_2")

    def test_str(self):
        root = Category.add_root(name="test")
        root.save()
        self.assertEqual(root.name, str(root))


class TestCategoryTrees(CategoryTestCaseMixin, TestCase):
    """django-treebeard related tests"""

    def test_create_in_mem_category(self):
        name = "Root Node"
        root = Category.add_root(name=name)
        root.set_current_language("en")
        self.assertEquals(root.name, "Root Node")

    def test_create_in_orm_category(self):
        name = "Root Node"
        root = Category.add_root(name=name)
        root.set_current_language("en")
        root.save()
        root = self.reload(root)
        self.assertEquals(root.name, name)

    def test_tree_depth(self):
        a = Category.add_root(name="A")
        b = a.add_child(name="B")
        c = b.add_child(name="C")
        self.assertEqual(c.depth, 3)

    def test_get_children_count(self):
        a = Category.add_root(name="A")
        a.add_child(name="B")
        self.assertEquals(a.get_children_count(), 1)
        a.add_child(name="C")
        a = self.reload(a)
        self.assertEquals(a.get_children_count(), 2)

    def test_get_children(self):
        a = Category.add_root(name="A")
        b = a.add_child(name="B")
        self.assertIn(b, a.get_children())
        c = a.add_child(name="C")
        a = self.reload(a)
        self.assertIn(c, a.get_children())

    def test_get_descendants(self):
        a = Category.add_root(name="A")
        b = a.add_child(name="B")
        c = b.add_child(name="C")
        self.assertIn(c, a.get_descendants())
        d = b.add_child(name='D')
        b = self.reload(b)
        self.assertIn(d, b.get_descendants())

    def test_get_ancestors(self):
        a = Category.add_root(name="A")
        b = a.add_child(name="B")
        c = b.add_child(name="C")
        self.assertIn(a, b.get_ancestors())
        self.assertIn(a, c.get_ancestors())
        d = b.add_child(name='D')
        self.assertIn(a, d.get_ancestors())

    def test_move_category(self):
        a = Category.add_root(name="A")
        b = a.add_child(name="B")
        c = a.add_child(name="C")
        a = self.reload(a)
        b = self.reload(b)
        self.assertEqual(a, c.get_parent())
        self.assertNotEqual(b, c.get_parent())
        c.move(b, "first-child")
        b = self.reload(b)
        c = self.reload(c)
        self.assertEqual(b, c.get_parent())


class TestCategoryParler(CategoryTestCaseMixin, TestCase):
    """django-parler related tests"""

    def test_add_translations(self):
        values = [
            # language code, name, slug
            ('en', "Cheese Omelette", "cheese-omelette"),
            ('de', "Käseomelett", "kaseomelett"),
            ('fr', "Omelette au Fromage", "omelette-au-fromage"),
        ]

        node = None

        # Create the translations
        for lang, name, slug in values:
            if node:
                with switch_language(node, lang):
                    node.name = name
                    node.save()
            else:
                with translation.override(lang):
                    node = Category.add_root(name=name)

        # Now test that they exist (and didn't obliterate one another)
        for lang, name, slug in values:
            with switch_language(node, lang):
                self.assertEqual(node.name, name)
                self.assertEqual(node.slug, slug)


class TestCategoryField(CategoryTestCaseMixin, TestCase):

    def test_category_multiple_choice_field(self):
        root = Category.add_root(name="root")
        root.save()
        child1 = root.add_child(name="child1")
        child2 = root.add_child(name="child2")
        grandchild1 = child1.add_child(name="grandchild1")
        root = self.reload(root)
        child1 = self.reload(child1)
        field = CategoryMultipleChoiceField(None)
        self.assertEqual(
            field.label_from_instance(child2),
            "&nbsp;&nbsp;child2",
        )
        self.assertEqual(
            field.label_from_instance(grandchild1),
            "&nbsp;&nbsp;&nbsp;&nbsp;grandchild1",
        )
        with self.assertRaises(ImproperlyConfigured):
            field.label_from_instance(object)

    def test_category_many_to_many_field(self):
        field = CategoryManyToManyField(Category)
        self.assertTrue(
            isinstance(field.formfield(), CategoryMultipleChoiceField)
        )
