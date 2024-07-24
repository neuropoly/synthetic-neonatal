path_dataset="/Users/amahlig/Documents/Maitrise/Git_repo/infant-brain-basel"

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

mkdir -p "${path_dataset}/derivatives/registered/"

for i in ${participants[@]}; do

    mkdir -p "${i}/"
    antsRegistrationSyNQuick.sh -f ${path_dataset}/${i}/anat/${i}_T1w.nii.gz \
    -m ${path_dataset}/${i}/anat/${i}_T2w.nii.gz -d 3 -o ${i}/ -t r

    antsApplyTransforms -d 3 -i ${path_dataset}/${i}/anat/${i}_T2w.nii.gz \
    -r ${path_dataset}/${i}/anat/${i}_T2w.nii.gz -o ${i}/${i}_T2w_R.nii.gz \
    -n Linear -v 1 -t ${i}/0GenericAffine.mat

    mkdir -p "${path_dataset}/derivatives/registered/${i}/"
    cp ${i}/${i}_T2w_R.nii.gz ${path_dataset}/derivatives/registered/${i}/${i}_T2wR.nii.gz

done

# Creating the dataset_description.json file for the registered images
jsonFilePath="${path_dataset}/derivatives/registered/dataset_description.json"
echo '{
  "Name": "T2w images registered to the T1w images of neonatal subjects",
  "BIDSVersion": "1.9.0",
  "License": "CC-by 4.0",
  "Description": "This folder contains the T2w images of the healthy neonatal subjects linearly registered to their respective T1w images.",
  "Tool": "ANTs"
}' > "$jsonFilePath"