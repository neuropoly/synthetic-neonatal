# python imports
import os
import keras
import numpy as np
import tensorflow as tf
from keras import models
import keras.callbacks as KC
from keras.optimizers import Adam
from inspect import getmembers, isclass
import sys

# project imports
path_synthsr = '/home/ge.polymtl.ca/almahj/SynthSR/'
sys.path.append(path_synthsr)
from SynthSR.brain_generator import BrainGenerator
from SynthSR.metrics_model import metrics_model, IdentityLoss, add_seg_loss_to_model
from SynthSR.training import training
from SynthSR.training import train_model

# third-party imports
from ext.lab2im import utils
from ext.lab2im import layers as l2i_layers
from ext.neuron import layers as nrn_layers
from ext.neuron import models as nrn_models

os.environ["CUDA_VISIBLE_DEVICES"]="1"

images_dir = path_synthsr + '/data/images/T2'
labels_dir = path_synthsr + 'data/labels/labels'
model_dir = path_synthsr + 'models/test1'

priors_means = np.load('/home/ge.polymtl.ca/almahj/SynthSR/images/labels_classes_priors/london_priors/prior_means.npy')
priors_stds = np.load('/home/ge.polymtl.ca/almahj/SynthSR/images/labels_classes_priors/london_priors/prior_stds.npy')

path_generation_labels = np.array([0, 24, 16, 4, 14, 15, 2, 12, 85, 3, 7, 8, 10, 11, 13, 17, 18, 26, 28, 42, 43, 46, 47, 49, 50, 52, 53, 54, 58, 60]) 
path_generation_classes = np.array([0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 7, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16])

training(labels_dir=labels_dir,
             model_dir=model_dir,
             prior_means=priors_means,
             prior_stds=priors_stds,
             path_generation_labels=path_generation_labels,
             segmentation_label_list=None,
             segmentation_label_equivalency=None,
             segmentation_model_file=None,
             fs_header_segnet=False,
             relative_weight_segmentation=0.25, 
             prior_distributions='normal',
             images_dir=images_dir,
             path_generation_classes=path_generation_classes,
             FS_sort=True,
             batchsize=1,
             input_channels=True,
             output_channel=None,
             target_res=np.array([1.6,1.6,5]),
             output_shape=None,
             flipping=False,
             padding_margin=None,
             scaling_bounds=0,
             rotation_bounds=0,
             shearing_bounds=0,
             translation_bounds=0,
             nonlin_std=0,
             nonlin_shape_factor=0, 
             simulate_registration_error=False,
             data_res=np.array([0.6,0.6,3]),
             thickness= np.array([0.6,0.6,3]),
             randomise_res=False,
             downsample=False,
             blur_range=1.15,
             build_reliability_maps=True,
             bias_field_std=.3,
             bias_shape_factor=0.03125,
             n_levels=5,
             nb_conv_per_level=2,
             conv_size=3,
             unet_feat_count=24,
             feat_multiplier=2,
             dropout=0,
             activation='elu',
             lr=1e-4,
             lr_decay=0,
             epochs=3, #100
             steps_per_epoch=5, #1000
             regression_metric='l1',
             work_with_residual_channel=None,
             loss_cropping=None,
             checkpoint=None,
             model_file_has_different_lhood_layer=False)

