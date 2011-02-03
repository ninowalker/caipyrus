from setuptools import setup, find_packages
import os.path, sys, subprocess

setup(  name='pypyrus',
        version='0.1',
        packages = ['pypyrus'],
        #install_requires=['pycairo'],
        zip_safe=True,
        test_suite='nose.collector',
        
        # metadata for upload to PyPI
        author = "Nino Walker",
        author_email = "nino@ni-no.info",
        description = "Cairo based procedural rendering tool.",
        license = "BSD",
        keywords = "OSM OpenStreetMap GTFS routing transit",
        url = "http://github.com/ninowalker/pypyrus/tree/master",
)
