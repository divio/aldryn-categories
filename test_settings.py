# -*- coding: utf-8 -*-
from __future__ import unicode_literals


HELPER_SETTINGS = {
    'SITE_ID': 1,
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'INSTALLED_APPS': [
        'parler',
        'treebeard',
        'aldryn_categories',
    ],
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de', },
            {'code': 'en', },
            {'code': 'fr', },
        ),
        'default': {
            # Do not remove or change this value or tests may break.
            'hide_untranslated': True,
            # Do not remove or change this value or tests may break.
            'fallback': 'fr',
        }
    }
}


def run():
    from djangocms_helper import runner
    runner.run('aldryn_categories')


if __name__ == "__main__":
    run()
