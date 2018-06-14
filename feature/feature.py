# -*- coding: utf-8 -*-
import csv
import operator
import numpy as np

from feature.motor_feature import MotorFeature
from feature.nonmotor_feature import NonMotorFeature

from numeric import isfloat, isint

class Feature(object):

    def __init__(self, filepath):
        self.motor = MotorFeature(filepath)
        self.nonmotor = NonMotorFeature(filepath)

        self.feature_name = {'motor':list(), 'nonmotor':list()}
        self.feature_list = list()
        self.feature_dict = dict()
        self.feature_len = 0
        self.feature_range = dict()


    def load_feature(self, ftype=None, fname=None, featname=None):
        try:
            if ftype == 'motor':
                self.motor.load_feature(fname, featname)
            elif ftype == 'nonmotor':
                self.nonmotor.load_feature(fname, featname)
        except ValueError:
            print ('the type should be one of Motor or Non-Motor')


    def load_label(self, ftype=None, fname=None, featname=None):
        try:
            if ftype == 'motor':
                return self.motor.load_label(fname, featname)
            elif ftype == 'nonmotor':
                return self.nonmotor.load_label(fname, featname)
        except ValueError:
            print ('the type should be one of Motor or Non-Motor, and the featname should be ny or mci')


    def get_feature_name(self, ftype=None):
        feature_name = dict() # variable type: feature name
        if ftype == 'motor':
            feature_name['motor'] = self.motor.feature_info.keys()
            self.feature_range = self.get_feature_range(ftype)
        elif ftype == 'nonmotor':
            feature_name['nonmotor'] = self.nonmotor.feature_info.keys()
            self.feature_range = self.get_feature_range(ftype)
        elif ftype == 'all':
            feature_name['motor'] = self.motor.feature_info.keys()
            self.feature_range.update(self.get_feature_range('motor'))
            feature_name['nonmotor'] = self.nonmotor.feature_info.keys()
            self.feature_range.update(self.get_feature_range('nonmotor'))
        self.feature_name = feature_name
        self.feature_list = list()
        for var_type, fn in self.feature_name.items():
            self.feature_list.extend(fn)
        self.feature_list = sorted(self.feature_list)
        self.feature_len = len(self.feature_list)
        self.feature_dict = dict(zip(self.feature_list, range(self.feature_len)))
        # print (self.feature_range)
        print (self.feature_list)


    def get_feature_range(self, ftype=None):
        if ftype == 'motor':
            return self.motor.get_feature_range()
        elif ftype == 'nonmotor':
            return self.nonmotor.get_feature_range()
