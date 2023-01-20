from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pdc/__init__.py
from pdc import __version__ as version

setup(
	name="pdc",
	version=version,
	description="pdc",
	author="Aqiq Solutions",
	author_email="info@aqiqsolutions.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
