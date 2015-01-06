# --*- coding: utf-8 -*-

from __future__ import unicode_literals

from operator import attrgetter

from django import VERSION
from django.contrib.contenttypes.models import ContentType
from django.db import models, router
from django.db.models.fields import Field
from django.db.models.related import RelatedObject
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from taggit.managers import (
    _TaggableManager,
    TaggableManager,
    TaggableRel,
)
from taggit.models import GenericTaggedItemBase
from taggit.utils import require_instance_manager

from .models import CategorisedItem

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:  # django < 1.7
    from django.contrib.contenttypes.generic import GenericRelation


def _model_name(model):
    if VERSION < (1, 7):
        return model._meta.module_name
    else:
        return model._meta.model_name


def _get_subclasses(model):
    subclasses = [model]
    for f in model._meta.get_all_field_names():
        field = model._meta.get_field_by_name(f)[0]
        if (isinstance(field, RelatedObject) and
                getattr(field.field.rel, "parent_link", None)):
            subclasses.extend(_get_subclasses(field.model))
    return subclasses


class _CategorisableManager(_TaggableManager):

    def get_queryset(self):
        try:
            return self.instance._prefetched_objects_cache[self.prefetch_cache_name]
        except (AttributeError, KeyError):
            return self.through.categories_for(self.model, self.instance)

    if VERSION < (1, 7):
        get_query_set = get_queryset

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is not None:
            raise ValueError("Custom queryset can't be used for this lookup.")

        instance = instances[0]
        from django.db import connections
        db = self._db or router.db_for_read(instance.__class__, instance=instance)

        fieldname = ('object_id' if issubclass(self.through, GenericTaggedItemBase)
                     else 'content_object')
        fk = self.through._meta.get_field(fieldname)
        query = {
            '%s__%s__in' % (self.through.category_relname(), fk.name):
                set(obj._get_pk_val() for obj in instances)
        }
        join_table = self.through._meta.db_table
        source_col = fk.column
        connection = connections[db]
        qn = connection.ops.quote_name
        qs = self.get_queryset().using(db)._next_is_sticky().filter(**query).extra(
            select={
                '_prefetch_related_val': '%s.%s' % (qn(join_table), qn(source_col))
            }
        )
        return (qs,
                attrgetter('_prefetch_related_val'),
                lambda obj: obj._get_pk_val(),
                False,
                self.prefetch_cache_name)

    @require_instance_manager
    def add(self, *categories):
        str_categories = set()
        category_objs = set()
        for c in categories:
            if isinstance(c, self.through.category_model()):
                category_objs.add(c)
            elif isinstance(c, six.string_types):
                str_categories.add(c)
            else:
                raise ValueError("Cannot add {0} ({1}). Expected {2} or str.".format(
                    c, type(c), type(self.through.category_model())))

        # If str_categories has 0 elements Django actually optimizes that to not do a
        # query.  Malcolm is very smart.
        existing = self.through.category_model().objects.filter(
            name__in=str_categories
        )
        category_objs.update(existing)

        for new_category in str_categories - set(c.name for c in existing):
            category_objs.add(self.through.category_model().objects.create(name=new_category))

        for category in category_objs:
            self.through.objects.get_or_create(category=category, **self._lookup_kwargs())

    @require_instance_manager
    def remove(self, *categories):
        self.through.objects.filter(**self._lookup_kwargs()).filter(
            category__name__in=categories).delete()

    def most_common(self):
        return self.get_queryset().annotate(
            num_times=models.Count(self.through.category_relname())
        ).order_by('-num_times')


class CategorisableManager(TaggableManager):
    _related_name_counter = 0

    def __init__(self,
                 verbose_name=_("Categories"),
                 help_text=_("A comma-separated list of categories."),
                 through=None, blank=False, related_name=None, to=None,
                 manager=_CategorisableManager):
        # NOTE: TaggableManager inherits from Field
        Field.__init__(self, verbose_name=verbose_name, help_text=help_text,
                       blank=blank, null=True, serialize=False)
        self.through = through or CategorisedItem
        self.rel = TaggableRel(self, related_name, self.through, to=to)
        self.swappable = False
        self.manager = manager
        # NOTE: `to` is ignored, only used via `deconstruct`.

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                             "before you can access their categories." % model.__name__)
        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            prefetch_cache_name=self.name
        )
        return manager

    def post_through_setup(self, cls):
        self.related = RelatedObject(cls, self.model, self)
        self.use_gfk = (
            self.through is None or issubclass(self.through, GenericTaggedItemBase)
        )
        if not self.rel.to:
            self.rel.to = self.through._meta.get_field("category").rel.to
        self.related = RelatedObject(self.through, cls, self)
        if self.use_gfk:
            categorised = GenericRelation(self.through)
            categorised.contribute_to_class(cls, 'categorised')

        for rel in cls._meta.local_many_to_many:
            if rel == self or not isinstance(rel, CategorisableManager):
                continue
            if rel.through == self.through:
                raise ValueError('You can\'t have two TaggableManagers or'
                                 ' CategorisableManagers with the same through'
                                 ' model.')

    def m2m_reverse_name(self):
        return self.through._meta.get_field_by_name("category")[0].column

    def m2m_reverse_field_name(self):
        return self.through._meta.get_field_by_name("category")[0].name

    def extra_filters(self, pieces, pos, negate):
        if negate or not self.use_gfk:
            return []
        prefix = "__".join(["categorised_items"] + pieces[:pos - 2])
        get = ContentType.objects.get_for_model
        cts = [get(obj) for obj in _get_subclasses(self.model)]
        if len(cts) == 1:
            return [("%s__content_type" % prefix, cts[0])]
        return [("%s__content_type__in" % prefix, cts)]
