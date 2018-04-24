import setuptools
import sys

if sys.version_info < (3, 0):
    raise EnvironmentError('Please install using pip3 or python3')

setuptools.setup(author='Chris Rosenthal',
                 author_email='crosenth@gmail.com',
                 description='Tools for visualizing ncbi taxonomic data',
                 keywords=['ncbi', 'rrndb', 'genetics', 'genomics'],
                 name='taxmagick',
                 packages=setuptools.find_packages(),
                 entry_points={
                     'console_scripts': [
                        'taxtree=taxmagick.tree:main',
                        'lineages=taxmagick.lineages:main']},
                 version=0.2,
                 url='https://github.com/crosenth/taxmagick',
                 license='GPLv3',
                 classifiers=[
                     'License :: OSI Approved :: '
                     'GNU General Public License v3 (GPLv3)',
                     'Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Operating System :: OS Independent',
                     'Intended Audience :: End Users/Desktop',
                     'License :: OSI Approved :: '
                     'GNU General Public License v3 (GPLv3)',
                     'Programming Language :: Python :: 3 :: Only'])
