import os
import sys
from access.resources.paths import REPO_DIR
from pathlib import Path

# split pipeline input into smaller files
complex_dir = sys.argv[1] #removed Path(REPO_DIR) + 
os.chdir(Path(REPO_DIR) / complex_dir)
os.system(f'split -C 20k summary.complex --additional-suffix=".complex"')
os.chdir(Path(REPO_DIR))
complex_files = [f for f in os.listdir(complex_dir) if os.path.isfile(os.path.join(complex_dir, f)) \
	and f != 'summary.complex' and f.endswith(".complex")]
num_new_files = len(complex_files)
print(num_new_files, ' new files generated')

# generate empty prediction files
for file in complex_files:
	prefix = file.split('.')[0]
	simple_file = prefix + '.simple'
	os.system(f'touch {complex_dir}/{simple_file}')
	# generate prediction files
	os.system(f'python3 scripts/generate.py < {complex_dir}/{file} > {complex_dir}/{simple_file}')
print('Generated predictions')

# combine prediction files
os.system(f'cat {complex_dir}/*.simple > {complex_dir}/summary.simple')

# remove split complex files (all complex files start with 'x')
os.system(f'rm {complex_dir}/x*')
print('Removed extraneous files')