from setuptools import setup, find_packages
import os.path
import re

VERSIONFILE = "eero/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

README_FILE = next(
    r
    for r in ['./README.txt', './README']
    if os.path.isfile(r)
)

setup(name='eero-km',
      version=verstr,
      description="Extract eero network details and insights",
      long_description=open(README_FILE, "r").read(),
      long_description_content_type="text/plain",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
      ],
      keywords='eero-km',
      author='Krishnadas Mallya',
      author_email='krishnadasmallya@gmail.com',
      url='https://github.com/krishnadasmallya/eero-client',
      license='MIT License',
      packages=find_packages(exclude=[
          'ez_setup', 'example', 'tests', 'external']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
          'click',
          'pandas',
          'PyYAML'
      ]
      )
