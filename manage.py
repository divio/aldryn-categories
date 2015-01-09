#!/usr/bin/env python

import django
from django.conf.urls import patterns

import app_manage

urlpatterns = patterns('')

if __name__ == '__main__':

    INSTALLED_APPS = [
        'parler',
        'treebeard',
        'aldryn_categories',
    ]

    if django.VERSION < (1, 7):
        INSTALLED_APPS += [
            'south',
        ]

    app_manage.main(
        ['aldryn_categories', ],
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=app_manage.DatabaseConfig(
            env='DATABASE_URL',
            arg='--db-url',
            default='sqlite://localhost/local.sqlite'
        ),
        SOUTH_MIGRATION_MODULES={
            'aldryn_categories': 'aldryn_categories.south_migrations',
        },
        ROOT_URLCONF='manage',
        STATIC_ROOT=app_manage.TempDir(),
        MEDIA_ROOT=app_manage.TempDir(),
    )
