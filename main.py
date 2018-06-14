#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, codecs
import numpy as np

from dataio import DataIO
from concatenation import Concatenation
from imputation import Imputation
from cligen import CliGen

import pickle as pkl

############################ DATA MANIPULATION ################################
def data_preprocess(params):
    ### Record Concatenation
    dataio = DataIO(params['input_path'], params['map_path'], params['domain'])
    dataio.read_data()
    dataio.read_label()
    ctn = Concatenation(dataio, params['domain'])
    patient_info, n_feature, feature_list, feature_range = ctn.get_concatenation()
                                           # patient id: Patient
                                           # static feature and dynamic feature
                                           # dynamic feature{time:feature_value}
    ### Data Imputation
    imp_method = 'simple'
    imp = Imputation(patient_info, n_feature)
    patient_array, patient_time = imp.get_imputation(imp_method)

    ### Clinical Data with DTI Generation
    cli = CliGen(feature_list, feature_range, ctn.dti_time)
    subject_array = cli.get_data(patient_array, patient_time, params['time'])
    if True == params['binary']: # only works for discrete clinical features
        subject_array = cli.get_binarization()
    subject_label = cli.get_label(patient_info, params['labels'], params['time'])
    return subject_array, subject_label

def save_clinic_records(params, subject_array, subject_label=None):
    f = open(params['domain'] + '.clinic.pkl', 'wb')
    pkl.dump(subject_array, f, -1)
    f.close()
    f = open(params['labels'] + '.pkl', 'wb')
    pkl.dump(subject_label, f, -1)
    f.close()

def main(params):
    subject_array, subject_label = data_preprocess(params)
    save_clinic_records(params, subject_array, subject_label)
    print ('Done!')

if __name__ == '__main__':
    main ({'domain': 'motor',
           'labels': 'hy',
           'input_path': 'data/',
           'map_path': 'map/',
           'time':'06/2016',
           'binary':True})
