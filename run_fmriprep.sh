
for_each -nthreads 6 BIDS_pan/sub-* : docker run -ti --rm \
    -v /home/clancy/ssd:/work \
    -u $(id -u):$(id -g) \
    -v /home/clancy/TemplateFlow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:24.1.1 \
    /work/BIDS_pan/ /work/fmriprep_pan/ participant --participant-label PRE \
	--skip_bids_validation \
	-w /work/fmriprep_work \
	--nthreads 1 --omp-nthreads 2 \
	--low-mem \
	--anat-only \
	--output-spaces MNI152NLin6Asym:res-2 \
	--skull-strip-fixed-seed \
	--skull-strip-t1w force \
	--fs-license-file /work/license.txt \
	--fs-subjects-dir /work/freesurfer_pan \
	--output-layout bids \
	--resource-monitor \
	--notrack \
	--stop-on-first-crash

