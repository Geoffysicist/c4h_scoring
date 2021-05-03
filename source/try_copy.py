import os
import shutil

try:
    source_readme = os.path.abspath('../../README.md')
    dest_readme = os.path.abspath('README.md')
    shutil.copy(source_readme, dest_readme)
except FileNotFoundError:
    print('{} file not found'.format(source_readme))
    
