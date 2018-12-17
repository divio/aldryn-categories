# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from aldryn_categories import __version__

# git tag '[version]'
# git push --tags origin master
# python setup.py sdist upload
# python setup.py bdist_wheel upload

setup(
    name='aldryn-categories',
    version=__version__,
    url='https://github.com/aldryn/aldryn-categories',
    license='BSD License',
    description='Hierarchical categories/taxonomies for your Django project',
    author='Divio AG',
    author_email='info@divio.ch',
    package_data={},
    packages=find_packages(),
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'django>=1.11',
        'django-parler',
        'django-treebeard',
        'aldryn-translation-tools',
    ],
    include_package_data=True,
    zip_safe=False
)
