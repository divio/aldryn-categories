[![](https://travis-ci.org/aldryn/aldryn-categories.svg?branch=master)](https://travis-ci.org/aldryn/aldryn-categories/)
[![Coverage Status](https://coveralls.io/repos/aldryn/aldryn-categories/badge.svg)](https://coveralls.io/r/aldryn/aldryn-categories)
[![](https://pypip.in/v/aldryn-categories/badge.svg)](https://pypi.python.org/pypi/aldryn-categories/)
[![](https://pypip.in/d/aldryn-categories/badge.svg)](https://pypi.python.org/pypi/aldryn-categories/)
[![](https://pypip.in/wheel/aldryn-categories/badge.svg)](https://pypi.python.org/pypi/aldryn-categories/)
[![](https://pypip.in/license/aldryn-categories/badge.svg)](https://github.com/aldryn/aldryn-categories/blob/master/LICENSE.txt)

# Aldryn Categories

Aldryn Categories is a simple project that provides hierarchical *categories* as
an independent model in your project. Categories are similar to *tags*, but are
structured into a taxonomy. The project is suitable for I18N projects as
Categories are fully translatable.


### Dependencies/Support

1. Python v2.7+
2. Django v1.6.x + South v1.0.2 or Django v1.7+
3. django-treebeard v2.0+
4. django-parler v1.2.1+


## Installation & Usage

To use Aldryn Categories, install the package with either:

	`pip install aldryn-categories`

Or directly from the GitHub repository with:

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