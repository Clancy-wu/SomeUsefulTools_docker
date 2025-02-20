all_subs=`ls BIDS | grep sub-`
mkdir xcpd_list
for i in ${all_subs}
do
    sub_dir=${i#sub-}
    touch xcpd_list/${sub_dir}
done    

for_each -nthreads 6 xcpd_list/* : docker run -ti --rm \
    -v /home/clancy/ssd:/work \
    -u $(id -u):$(id -g) \
    -v /home/clancy/TemplateFlow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
	pennlinc/xcp_d:latest \
	/work/fmriprep/ /work/xcpd/ participant --participant-label PRE \
	--mode linc \
	--nthreads 1 --omp-nthreads 2 --mem-gb 10 \
	--input-type fmriprep \
	--file-format nifti \
	--dummy-scans auto \
	--despike n \
	-p 36P \
	--smoothing 6 \
	--combine_runs n \
	--lower-bpf 0.01 \
	--upper-bpf 0.08 \
	--fd-thresh 0 \
	--min-time 0 \
	--linc_qc n \
	--skip-parcellation \
	-w /work/xcpd_work \
	--fs-license-file /work/license.txt \
	--resource-monitor \
	--stop-on-first-crash 

rm xcpd_list

