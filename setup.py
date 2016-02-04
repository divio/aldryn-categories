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
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'django>=1.6,<1.10',
        'django-parler>=1.2.1',
        'django-treebeard>=2.0',
        'aldryn-translation-tools>=0.2.1,<0.3',
    ],
    include_package_data=True,
    zip_safe=False
)
