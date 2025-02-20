import os
from glob import glob
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from nilearn import image
import pandas as pd

def run(f, this_iter):
    with ProcessPoolExecutor(max_workers=14) as executor:
        results = list(tqdm(executor.map(f, this_iter), total=len(this_iter)))
    return results

def get_36P(bold_mni_name):
    replace_bold = 'space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii.gz'
    replace_confound = 'desc-confounds_timeseries.tsv'
    confounds_file = bold_mni_name.replace(replace_bold, replace_confound)
    confound_df = pd.read_csv(confounds_file, sep='\t')
    P36 = ['trans_x', 'trans_x_derivative1', 'trans_x_derivative1_power2', 'trans_x_power2',
        'trans_y', 'trans_y_derivative1', 'trans_y_derivative1_power2', 'trans_y_power2',
        'trans_z', 'trans_z_derivative1', 'trans_z_derivative1_power2', 'trans_z_power2',
        'rot_x', 'rot_x_derivative1', 'rot_x_power2', 'rot_x_derivative1_power2',
        'rot_y', 'rot_y_derivative1', 'rot_y_power2', 'rot_y_derivative1_power2',
        'rot_z', 'rot_z_derivative1', 'rot_z_power2', 'rot_z_derivative1_power2',
        'global_signal', 'global_signal_derivative1', 'global_signal_power2', 'global_signal_derivative1_power2',
        'csf', 'csf_derivative1', 'csf_power2', 'csf_derivative1_power2',
        'white_matter', 'white_matter_derivative1', 'white_matter_power2', 'white_matter_derivative1_power2',
        ]
    out_df = confound_df.loc[:, P36]
    out_df = out_df.fillna(0)
    return out_df
##############
bids_dir = 'BIDS'
fmrip_dir = 'fmriprep'
temp_3mm = '/home/clancy/TemplateFlow/BN_Atlas_for_FSL/BN_Atlas_246_3mm.nii.gz' # LAS
out_1 = 'Results/TARWDC'
out_2 = 'Results/TARWDCF'
out_3 = 'Results/TARWDCS'
##############
def create_out_1(sub_name):
    bold_mni = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii.gz'
    bold_mask = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-brain_mask.nii.gz'
    bold_confound = get_36P(bold_mni)
    out_img = image.clean_img(bold_mni, detrend=True, standardize=True, confounds=bold_confound, 
                    low_pass=None, high_pass=None, t_r=2, ensure_finite=False, mask_img=bold_mask)
    out_img_3mm = image.resample_to_img(source_img=out_img, target_img=temp_3mm, interpolation='continuous')
    sub_name_new = sub_name.replace('sub-', '')
    out_img_name = f'{out_1}/{sub_name_new}/TARWDC_{sub_name_new}.nii'
    os.makedirs(os.path.dirname(out_img_name), exist_ok=True)
    out_img_3mm.to_filename(out_img_name)
    return 0
def create_out_2(sub_name):
    bold_mni = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii.gz'
    bold_mask = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-brain_mask.nii.gz'
    bold_confound = get_36P(bold_mni)
    out_img = image.clean_img(bold_mni, detrend=True, standardize=True, confounds=bold_confound, 
                    low_pass=0.08, high_pass=0.01, t_r=2, ensure_finite=False, mask_img=bold_mask)
    out_img_3mm = image.resample_to_img(source_img=out_img, target_img=temp_3mm, interpolation='continuous')
    sub_name_new = sub_name.replace('sub-', '')
    out_img_name = f'{out_2}/{sub_name_new}/TARWDCF_{sub_name_new}.nii'
    os.makedirs(os.path.dirname(out_img_name), exist_ok=True)
    out_img_3mm.to_filename(out_img_name)
    return 0    
def create_out_3(sub_name):
    # 'Results/TARWDCS'
    bold_mni = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-preproc_bold.nii.gz'
    bold_mask = f'{fmrip_dir}/{sub_name}/func/{sub_name}_task-rest_space-MNI152NLin6Asym_res-2_desc-brain_mask.nii.gz'
    bold_confound = get_36P(bold_mni)
    out_img = image.clean_img(bold_mni, detrend=True, standardize=True, confounds=bold_confound, 
                    low_pass=None, high_pass=None, t_r=2, ensure_finite=False, mask_img=bold_mask)
    out_img_3mm = image.resample_to_img(source_img=out_img, target_img=temp_3mm, interpolation='continuous')
    out_img_3mmS = image.smooth_img(out_img_3mm, fwhm=6)
    sub_name_new = sub_name.replace('sub-', '')
    out_img_name = f'{out_3}/{sub_name_new}/TARWDCS_{sub_name_new}.nii'
    os.makedirs(os.path.dirname(out_img_name), exist_ok=True)
    out_img_3mmS.to_filename(out_img_name)
    return 0

if __name__ == '__main__':
    all_subs = [x for x in os.listdir(bids_dir) if 'sub-' in x]
    aa = run(create_out_1, all_subs)
    aa = run(create_out_2, all_subs)
    aa = run(create_out_3, all_subs)
    print('finished.')