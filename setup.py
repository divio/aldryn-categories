# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from aldryn_categories import __version__

REQUIREMENTS = [
    'django-treebeard>=2.0',
    'django-parler>=1.2.1',
    # git tag '[version]'
    # git push --tags origin master
    # python setup.py sdist upload
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-categories',
    version=__version__,
    description='Heirarchical categories',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-categories',
    packages=find_packages(),
    package_data={},
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
