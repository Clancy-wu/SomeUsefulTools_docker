!#/bin/bash
for_each -nthreads 3 BIDS/sub-* : docker run -ti --rm \
    -v /home/clancy/ssd:/work \
    -u $(id -u):$(id -g) \
    -v /home/clancy/TemplateFlow:/opt/templateflow \
    -e TEMPLATEFLOW_HOME=/opt/templateflow \
    nipreps/fmriprep:24.1.1 \
    /work/BIDS/ /work/fmriprep/ participant --participant-label PRE \
	--skip_bids_validation \
	--ignore fieldmaps \
	-w /work/fmriprep_work \
	--nthreads 2 --omp-nthreads 2 \
	--output-spaces MNI152NLin6Asym:res-2 \
	--force-no-bbr \
	--fs-license-file /work/license.txt \
	--fs-no-reconall \
	--output-layout bids \
	--resource-monitor \
	--notrack \
	--stop-on-first-crash

