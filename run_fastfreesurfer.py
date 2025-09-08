import os
from glob import glob
from shutil import copy
#from nilearn import image

#from concurrent.futures import ProcessPoolExecutor
#from tqdm import tqdm
#def run(f, this_iter):
#    with ProcessPoolExecutor(max_workers=10) as executor:
#        results = list(tqdm(executor.map(f, this_iter), total=len(this_iter)))
#    return results

fast_dir = 'fastfreesurfer'
#t1_dir = f'{fast_dir}/anat'
#os.makedirs(t1_dir, exist_ok=True)

#t1_files = glob('BIDS/sub-*/anat/sub-*_T1w.nii.gz')
#for t1 in t1_files:
#    t1_new = os.path.join(t1_dir, os.path.basename(t1))
#    t1_new = t1_new.replace('.nii.gz', '.nii')
#    image.load_img(t1).to_filename(t1_new)
#print('finished')
    
fastfree_dir = f'{fast_dir}/freesurfer'
os.makedirs(fastfree_dir, exist_ok=True)

all_subs = [x for x in os.listdir('BIDS') if 'sub-' in x]

def run_fastfreesurfer_command(sub_name):
	my_command = f"docker run --gpus all -v /home/clancy/ssd/SCH/fastfreesurfer:/data \
						--rm --user $(id -u):$(id -g) deepmi/fastsurfer:latest \
						--fs_license /data/license.txt \
						--t1 /data/anat/{sub_name}_T1w.nii \
						--sid {sub_name} --sd /data/freesurfer \
						--3T \
						--threads 4 " 
	return my_command

i = 1
for sub_name in all_subs:
	print(i)
	sub_command = run_fastfreesurfer_command(sub_name)
	os.system(sub_command)
	i += 1

print('finished. ')
