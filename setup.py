from setuptools import setup, find_packages
import sys, os
import vogelerunner

version = vogelerunner.__version__

setup(name='vogelerunner',
      version=version,
      description="Python-based Configuration Management Framework, Runner part",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='cmdb management',
      author='Luc Stepniewski',
      author_email='luc.stepniewski@adelux.fr',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
#      package_data = {
#          'vogelerunnerdata': ['data/*',],
#      },
      tests_require='nose',
      test_suite='nose.collector',

      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'couchdb',
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      vogelerunner = vogelerunner.command:main
      """,
      )
