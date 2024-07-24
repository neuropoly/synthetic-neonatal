#!/bin/bash

# This script segments the neonatal brain images of the basel dataset using the SAMSEG algorithm.
# To be run inside the SynthSR folder.

path_dataset="/home/ge.polymtl.ca/almahj/datasets/infant-brain-basel"
path_home="/home/ge.polymtl.ca/almahj"

# Select the healthy neonatal subjects
participants=()
while IFS=$'\t' read -r -a line; do
    if [[ ${line[0]} == *"sub-"* ]] && [[ ${line[2]} == "normal" ]] && [[ ${line[1]} == "0" ]]; then
        # These subjects have artifacts in their images.
        if [[ ${line[0]} != "sub-0544" && ${line[0]} != "sub-0623" && ${line[0]} != "sub-0645" && ${line[0]} \
        != "sub-0672" && ${line[0]} != "sub-0732" && ${line[0]} != "sub-0841" ]]; then
            participants+=("${line[0]}")
        fi
    fi
done <"${path_dataset}/participants.tsv"

#Create separate folders for T1,T2 and labels as required by the SynthSR script
mkdir -p ${path_home}/SynthSR/data/images/T1/
mkdir -p ${path_home}/SynthSR/data/images/T2/
mkdir -p ${path_home}/SynthSR/data/labels/labels/

for i in ${participants[@]}; do

    # Copy the T1w and T2wR images to the SynthSR folder
    cp "${path_dataset}/${i}/anat/${i}_T1w.nii.gz" "${path_home}/SynthSR/data/images/T1/"
    cp "${path_dataset}/derivatives/registered/${i}/${i}_T2wR.nii.gz" "${path_home}/SynthSR/data/images/T2/${i}_T2w.nii.gz"

    # Segment the images
    mkdir -p "${path_home}/Segmentation/samseg/basel/${i}/"
    run_samseg --input "${path_dataset}/${i}/anat/${i}_T1w.nii.gz" "${path_dataset}/${i}/anat/${i}_T2w.nii.gz" \
    --output "${path_home}/Segmentation/samseg/basel/${i}/"

    # Copy the labels to the SynthSR folder
    cp "${path_home}/Segmentation/samseg/basel/${i}/seg.mgz" "${path_home}/SynthSR/data/labels/labels/${i}_labels.mgz"

    # Put the results in the derivatives folder of the dataset
    # mkdir -p "${path_dataset}/derivatives/segmentation/${i}/anat/"
    # cp "${path_home}/Segmentation/samseg/basel/${i}/seg.mgz" "${path_dataset}/derivatives/segmentation/${i}/anat/${i}_seg.mgz"

done
