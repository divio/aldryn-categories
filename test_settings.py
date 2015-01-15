HELPER_SETTINGS = {
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
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_categories')

if __name__ == "__main__":
    run()
