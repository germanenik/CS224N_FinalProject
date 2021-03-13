import os
import sys
from access.resources.paths import REPO_DIR

# split .complex into smaller files
#os.system('source venv/bin/activate')
#generate_dir = Path(REPO_DIR) + scripts
complex_dir = sys.argv[1] #removed Path(REPO_DIR) + 
print(complex_dir)
os.system(f'split -C 30k {complex_dir}/pipeline.complex --additional-suffix=".complex"')
print(os.listdir(complex_dir))
complex_files = [f for f in os.listdir(complex_dir) if os.path.isfile(os.path.join(complex_dir, f)) and f != 'pipeline.complex']
num_new_files = len(complex_files)
print(num_new_files) # should be 8

# generate empty prediction files
for file in complex_files:
	prefix = file.split('.')[0]
	simple_file = prefix + '.simple'
	os.system(f'touch {complex_dir}/{simple_file}')
	# generate prediction files
	os.system(f'python3 scripts/generate.py < {complex_dir}/{file} > {complex_dir}/{simple_file}')

# combine prediction files
os.system(f'cat {complex_dir}/*.simple > {complex_dir}/pipeline_valerror.simple')

# remove split complex files (all complex files start with 'x')
os.system(f'rm {complex_dir}/x*')