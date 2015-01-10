# Aldryn Categories

## Project Goals

1. Provide a heirarchical categorizing capability that could be used to tag arbitrary
   content throughout a project with a common set of categories.
2. Categories should be Internationalizable.
3. Should be largely compatible with (but decoupled from) django-taggit.
4. Should be extensible: possible to extend the base tag/category model to add arbitrary
   fields/methods.

### Dependencies/Support

1. Python v2.7+
2. Django v1.6.x + South v1.0.2 or Django v1.7+
3. django-treebeard v2.0+
4. django-parler v1.2.1+


## Usage

To use Aldryn Categories, install the package (currently, only available from
its GitHub repository) with:

	`pip install https://github.com/aldryn/aldryn-categories/archive/master.zip`

Next, add `aldryn_categories` to your `INSTALLED_APPS`.

Now, add a `CategoryManyToManyField` to `aldryn_categories.Category` on any
models you wish to categorize, like so:

	# -*- coding: utf-8 -*-

	from django.db import models
	from aldryn_categories.fields import CategoryManyToManyField

	class Thing(models.Model):
	    my_field = models.CharField(...)
	    ...
	    categories = CategoryManyToManyField('aldryn_categories.Category')

This usage of the CategoryManyToManyField simply allows your categories to be
displayed heirarchically in the otherwise normal MultipleSelectWidget like so:

![](diagrams/category-widget-preview.png?raw=true)