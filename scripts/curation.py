# This script adds the necessary padding to a dataset so that all images have the same dimensions.

import nibabel as nib
import numpy as np
import os

def get_nifti_dimensions(directory):
    dimensions = []
    target_subdir = os.path.join(directory, 'derivatives', 'registered')
    for root, _, files in os.walk(target_subdir):
        for filename in files:
            if filename.endswith('.nii') or filename.endswith('.nii.gz'):
                filepath = os.path.join(root, filename)
                img = nib.load(filepath)
                dimensions.append((filepath, img.shape))
    return dimensions

def extract_subject_name(filepath):
    parts = filepath.split(os.sep)
    for part in parts:
        if part.startswith('sub-'):
            return part
    return "Unknown"

def calculate_max_dimensions(dimensions):
    max_shape = np.max([dim[1] for dim in dimensions], axis=0)
    return max_shape

def add_padding(directory, target_shape):
    target_subdir = os.path.join(directory, 'derivatives', 'registered')
    for root, _, files in os.walk(target_subdir):
        for filename in files:
            if filename.endswith('.nii') or filename.endswith('.nii.gz'):
                filepath = os.path.join(root, filename)
                img = nib.load(filepath)
                data = img.get_fdata()
                
                pad_widths = [(0, max(0, target - current)) for target, current in zip(target_shape, data.shape)]
                padded_data = np.pad(data, pad_widths, mode='constant', constant_values=0)
                padded_img = nib.Nifti1Image(padded_data, img.affine, img.header)

                padded_filepath = os.path.join(root, f"padded_{filename}")
                nib.save(padded_img, padded_filepath)


directory = '/home/ge.polymtl.ca/almahj/datasets/infant-brain-basel/'
dimensions = get_nifti_dimensions(directory)

target_shape = calculate_max_dimensions(dimensions)
print(f"Target shape for padding: {target_shape}")

add_padding(directory, target_shape)