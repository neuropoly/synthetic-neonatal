## Prior estimations for the GMM

import sys
import numpy as np
import nibabel as nib
import os
path_synthsr = '/home/ge.polymtl.ca/almahj/SynthSR/'
sys.path.append(path_synthsr)
from SynthSR.estimate_priors import build_intensity_stats

images_dir = [path_synthsr + 'data/images/T1/', path_synthsr + '/data/images/T2/']
labels_dir = path_synthsr + 'data/labels/labels/'

#Remove labels 165, 258, 24, 77 and 80 from all the segmented images
labels_to_delete = [165, 258, 24, 77, 80]
label_files = [os.path.join(labels_dir, f) for f in os.listdir(labels_dir) if f.endswith('.mgz')]

for img_path in label_files:
    img = nib.load(img_path)
    data = img.get_fdata()
    for label in labels_to_delete:
        data[data == label] = 0

    new_img = nib.MGHImage(data, img.affine, img.header)
    nib.save(new_img, img_path)
    

# Numpy arrays with the labels corresponding to samseg
estimation_labels = np.array([0, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 28, 30, 31, 41, 42, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 58, 60, 62, 63, 72, 85]) #Labels in samseg, minus 165, 258, 24, 77 et 80
estimation_classes = np.array([0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 3, 3, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 3, 17]) # Classes grouping left/right labels and the ventricules

result_dir = path_synthsr + 'images/labels_classes_priors/basel_priors/'

build_intensity_stats(list_image_dir=images_dir,
                      list_labels_dir=labels_dir,
                      estimation_labels=estimation_labels,
                      estimation_classes=estimation_classes,
                      result_dir=result_dir,
                      rescale=True)