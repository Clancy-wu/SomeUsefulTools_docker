#!/bin/bash
date

docker run --gpus all -v /home/clancy/ssd/yuhang:/data \
                      --rm --user $(id -u):$(id -g) deepmi/fastsurfer:latest \
                      --fs_license /data/license.txt \
                      --t1 /data/T1_one/JKR19/anat.nii \
                      --sid JKR19 --sd /data/T1_surf \
                      --3T \
                      --threads 4
                      
date
