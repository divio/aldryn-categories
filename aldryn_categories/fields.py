# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# import warnings

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.utils.safestring import mark_safe

# For South, where used.
try:
    from south.modelsinspector import add_introspection_rules
except:
    add_introspection_rules = False


class CategoryMultipleChoiceField(ModelMultipleChoiceField):
    """Displays choices heirarchically as per their position in the tree."""
    def label_from_instance(self, obj):
        prefix = ''
        try:
            if obj.depth > 1:
                prefix = '&nbsp;&nbsp;' * (obj.depth - 1)

            return mark_safe("{prefix}{name}".format(
                prefix=prefix, name=obj.name
            ))
        except:
            raise ImproperlyConfigured(
                "CategoryMultipleChoiceField should only be used for M2M "
                "relations to the aldryn_categories.Category model.")


class CategoryManyToManyField(ManyToManyField):
    """Simply a normal ManyToManyField, but with a custom *default* form field
    which has a heirarchically displayed set of choices.
    """
    def formfield(self, form_class=CategoryMultipleChoiceField,
                  choices_form_class=None, **kwargs):
        kwargs["form_class"] = form_class
        kwargs["choices_form_class"] = choices_form_class
        return super(CategoryManyToManyField, self).formfield(**kwargs)


if add_introspection_rules:
    add_introspection_rules([], [
        "^aldryn_categories\.fields\.CategoryManyToManyField"
    ])
