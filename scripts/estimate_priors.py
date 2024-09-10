## Prior estimations for the GMM

import sys
import numpy as np
import os
path_synthsr = '/home/ge.polymtl.ca/almahj/SynthSR/'
sys.path.append(path_synthsr)
from SynthSR.estimate_priors import build_intensity_stats

images_dir = [path_synthsr + 'data/images/HYP/']
labels_dir = [path_synthsr + 'data/labels/HYP/']

# Numpy arrays with the labels corresponding to samseg
estimation_labels = np.array([0, 24, 16, 4, 14, 15, 2, 12, 85, 3, 7, 8, 10, 11, 13, 17, 18, 26, 28, 42, 43, 46, 47, 49, 50, 52, 53, 54, 58, 60]) 
estimation_classes = np.array([0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 7, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16]) # Classes grouping left/right labels and the ventricules

result_dir = path_synthsr + 'images/labels_classes_priors/london_priors/'

build_intensity_stats(list_image_dir=images_dir,
                      list_labels_dir=labels_dir,
                      estimation_labels=estimation_labels,
                      estimation_classes=estimation_classes,
                      result_dir=result_dir,
                      rescale=True)