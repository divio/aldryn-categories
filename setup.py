# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from aldryn_categories import __version__

# git tag '[version]'
# git push --tags origin master
# python setup.py sdist upload

setup(
    name='aldryn-categories',
    version=__version__,
    url='https://github.com/aldryn/aldryn-categories',
    license='LICENSE.txt',
    description='Heirarchical categories/taxonomies for your Django project',
    long_description=open('README.md').read(),
    author='Divio AG',
    author_email='info@divio.ch',
    package_data={},
    packages=find_packages(),
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
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
        'django-parler>=1.2.1',
        'django-treebeard>=2.0',
    ],
    include_package_data=True,
    zip_safe=False
)
