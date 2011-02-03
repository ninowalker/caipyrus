from setuptools import setup, find_packages
import os.path, sys, subprocess

setup(  name='caipyrus',
        version='0.1',
        packages = ['caipyrus'],
        zip_safe=True,
        test_suite='nose.collector',
        
        # metadata for upload to PyPI
        author = "Nino Walker",
        author_email = "nino@ni-no.info",
        description = "Cairo based procedural rendering tool.",
        license = "BSD",
        keywords = "OSM OpenStreetMap GTFS routing transit",
        url = "http://github.com/ninowalker/caipyrus/tree/master",
)
