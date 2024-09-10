# This script generates synthetic LF images from a HF dataset.

import numpy as np
import sys
import os
path_synthsr = '/home/ge.polymtl.ca/almahj/SynthSR/'
sys.path.append(path_synthsr)
from SynthSR.brain_generator import BrainGenerator
from ext.lab2im import utils

images_dir = path_synthsr + '/data/images/T2'
labels_dir = path_synthsr + 'data/labels/labels'

priors_means = np.load('/home/ge.polymtl.ca/almahj/SynthSR/images/labels_classes_priors/london_priors/prior_means.npy')
priors_stds = np.load('/home/ge.polymtl.ca/almahj/SynthSR/images/labels_classes_priors/london_priors/prior_stds.npy')

estimation_labels = np.array([0, 24, 16, 4, 14, 15, 2, 12, 85, 3, 7, 8, 10, 11, 13, 17, 18, 26, 28, 42, 43, 46, 47, 49, 50, 52, 53, 54, 58, 60]) 
estimation_classes = np.array([0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 7, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16])

brain_generator = BrainGenerator(labels_dir=labels_dir,
                 prior_means=priors_means,
                 prior_stds=priors_stds,
                 prior_distributions="normal",
                 generation_labels=estimation_labels,
                 images_dir=images_dir,
                 n_neutral_labels=6,
                 padding_margin=None,
                 batchsize=1,
                 input_channels=1,
                 output_channel=None,
                 target_res=(1.6,1.6,5.0), 
                 output_shape=None,
                 output_div_by_n=None,
                 generation_classes=estimation_classes,
                 flipping=False, 
                 scaling_bounds=0,
                 rotation_bounds=0,
                 shearing_bounds=0,
                 translation_bounds=0,
                 nonlin_std=0,
                 nonlin_shape_factor=0,
                 simulate_registration_error=False, 
                 randomise_res=False, 
                 data_res=None,
                 thickness=None,
                 downsample=True,
                 blur_range=1.15, 
                 build_reliability_maps=False,
                 bias_field_std=0.3,
                 bias_shape_factor=0.025) 

image,target = brain_generator.generate_brain()

nb_images = 55
result_dir = path_synthsr + 'synthetic'

for n in range(nb_images):

    utils.save_volume(np.squeeze(image[..., 2]), brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 't2_input_%s.nii.gz' % (n + 1)))
    utils.save_volume(np.squeeze(target), brain_generator.aff, brain_generator.header,
                      os.path.join(result_dir, 'synthetic_target_%s.nii.gz' % (n + 1)))