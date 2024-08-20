# This script changes the labels of the segmentation files done with WMHSynthSeg and Samseg to make them correspond

import nibabel as nib
import os
import glob

## WMH file

seg_fileWMH = os.path.join('/Users/amahlig/Documents/Maitrise/IRM/Resultats', 'segWMH_london.nii')
segWMH = nib.load(seg_fileWMH)
seg_dataWMH = segWMH.get_fdata()

# Labels change

# Right-cerebral-white-matter will be fusioned with Left-cerebral-white-matter
seg_dataWMH[seg_dataWMH == 41] = 2
# WM-hypointensities will be fusioned also with Left-cerebral-white-matter
# WM-hypointensities is a non-sided label, therefore the cerebral-white-matter is fusionned into one label to also integrate the WMH
seg_dataWMH[seg_dataWMH == 77] = 2
# Right-Putamen will be fusioned with Left-Putamen as per what is one below
seg_dataWMH[seg_dataWMH == 51] = 12


seg_newWMH = nib.Nifti1Image(seg_dataWMH, segWMH.affine)
output_fileWMH = os.path.join('/Users/amahlig/Documents/Maitrise/IRM/Resultats', 'segWMH_london_newlabels.nii')
nib.save(seg_newWMH, output_fileWMH)


## Samseg files

seg_filesSS = glob.glob('/Users/amahlig/Documents/Maitrise/IRM/Datasets/basel_bid/derivatives/segmentation/*/anat/sub-*_seg.mgz')

for seg_file in seg_filesSS:
    segSS = nib.load(seg_file)
    seg_dataSS = segSS.get_fdata()

    # Labels change

    # Left-Inf-Lat-Vent will be fusioned with Left-Lateral-Ventricle, same with right side
    seg_dataSS[seg_dataSS == 5] = 4
    seg_dataSS[seg_dataSS == 44] = 43
    # Left-vessel will be fusioned with Left-Putamen, same with right side
    seg_dataSS[seg_dataSS == 30] = 12
    seg_dataSS[seg_dataSS == 62] = 51
    # Left-choroid-plexus will be fusioned with the 4th-Ventricule, same with right side
    seg_dataSS[seg_dataSS == 31] = 15
    seg_dataSS[seg_dataSS == 63] = 15
    # The 5th-Ventricle will be fusioned with the 4th-Ventricle
    seg_dataSS[seg_dataSS == 72] = 15
    # Right-cerebral-white-matter and WM-hypointensities will also be fusioned with Left-cerebral-white-matter for the same reason as above.
    seg_dataSS[seg_dataSS == 41] = 2
    seg_dataSS[seg_dataSS == 77] = 2
    # non-WM-hypointensities will be fusioned with the putamen. Since it is a sided-label, the Right-Putamen and Left-Putamen will also be fusioned.
    seg_dataSS[seg_dataSS == 51] = 12
    seg_dataSS[seg_dataSS == 80] = 12
    # The labels Skull and Soft-Nonbrain-Tissue will be removed
    seg_dataSS[seg_dataSS == 165] = 0
    seg_dataSS[seg_dataSS == 258] = 0


    seg_newSS = nib.Nifti1Image(seg_dataSS, segSS.affine)
    output_fileSS = seg_file.replace('_seg.mgz', '_seg_newlabels.nii')
    nib.save(seg_newSS, output_fileSS)