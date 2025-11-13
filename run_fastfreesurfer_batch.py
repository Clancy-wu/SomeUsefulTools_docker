import os
from glob import glob
from shutil import copy
from nilearn import image

def run_fastfreesurfer_command(sub_name):
	my_command = f"docker run --gpus all -v /home/clancy/ssd/SCH/fastfreesurfer:/data \
						--rm --user $(id -u):$(id -g) deepmi/fastsurfer:latest \
						--fs_license /data/license.txt \
						--t1 /data/anat/{sub_name}/{sub_name}_T1w.nii \
						--sid {sub_name} --sd /data/freesurfer \
						--3T \
						--threads 4 " 
	return my_command

fast_dir = 'fastfreesurfer'
t1_dir = f'{fast_dir}/anat'
os.makedirs(t1_dir, exist_ok=True)
free_dir = f'{fast_dir}/freesurfer'
os.makedirs(free_dir, exist_ok=True)

all_subs = [x for x in os.listdir('BIDS') if 'sub-' in x]
copy('license.txt', f'{fast_dir}/license.txt')

i = 1
for sub_name in all_subs:
	t1_old = f'BIDS/{sub_name}/anat/{sub_name}_T1w.nii.gz'
	t1_new = f'fastfreesurfer/anat/{sub_name}/{sub_name}_T1w.nii'
	os.makedirs(os.path.dirname(t1_new), exist_ok=True)
	image.load_img(t1_old).to_filename(t1_new)
	sub_command = run_fastfreesurfer_command(sub_name)
	os.system(sub_command)
	i += 1

print('finished. ')
