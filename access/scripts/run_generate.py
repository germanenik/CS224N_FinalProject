import os
import sys
from access.resources.paths import REPO_DIR
from pathlib import Path

# split .complex into smaller files
#os.system('source venv/bin/activate')
#generate_dir = Path(REPO_DIR) + scripts
complex_dir = sys.argv[1] #removed Path(REPO_DIR) + 
print(complex_dir)
#os.system(f'cd {complex_dir}')
os.chdir(Path(REPO_DIR) / complex_dir)
os.system('ls')
os.system('pwd')
os.system(f'split -C 30k pipeline.complex --additional-suffix=".complex"')
os.chdir(Path(REPO_DIR))
os.system('pwd')
print(os.listdir(complex_dir))
complex_files = [f for f in os.listdir(complex_dir) if os.path.isfile(os.path.join(complex_dir, f)) \
	and f != 'pipeline.complex' and f.endswith(".complex")]
num_new_files = len(complex_files)
print(num_new_files) # should be 8

# generate empty prediction files
'''for file in complex_files:
	prefix = file.split('.')[0]
	simple_file = prefix + '.simple'
	os.system(f'touch {complex_dir}/{simple_file}')
	# generate prediction files
	os.system(f'python3 scripts/generate.py < {complex_dir}/{file} > {complex_dir}/{simple_file}')

# combine prediction files
os.system(f'cat {complex_dir}/*.simple > {complex_dir}/pipeline_valerror.simple')

# remove split complex files (all complex files start with 'x')
os.system(f'rm {complex_dir}/x*')'''