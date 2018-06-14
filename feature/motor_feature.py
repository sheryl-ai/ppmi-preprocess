# -*- coding: utf-8 -*-

import sys
import math
import csv, codecs
import operator

from numeric import isint, isfloat
from time_converter import convert_time, convert_int


class MotorFeature(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        self.label_info = list()


    def load_feature(self, fname=None, featname=None):
        try:
            if fname == 'MDS UPDRS PartII':
                self.read_feature('motor/MDS_UPDRS_Part_II__Patient_Questionnaire.csv', date_key='INFODT')
            elif fname == 'MDS UPDRS PartIII':
                self.read_feature('motor/MDS_UPDRS_Part_III__Post_Dose_.csv', featname, date_key='INFODT')
        except ValueError:
            print ('please enter correct file name')

    def load_label(self, fname=None, featname=None):
        try:
            if fname == 'MDS UPDRS PartIII':
                self.read_feature('motor/MDS_UPDRS_Part_III__Post_Dose_.csv', featname, date_key='INFODT')
                # print (self.feature_info)
                self.label_info = self.feature_info['NHY']
                return self.label_info
        except ValueError:
            print ('please enter correct file name')

    def read_feature(self, filename, featname=None, time_convert=False, date_key=None, pid_name='PATNO'):
        fname = self.get_feature_name(filename, featname)
        f = codecs.open(self.filepath + filename, 'r', 'utf-8')
        reader = csv.reader(f)
        line_ctr = 0
        for row in reader:
            # table title
            if line_ctr < 1:
                table_ttl = dict(zip(row, range(len(row))))
                for fn in fname:
                    self.feature_info[fn] = list()
                line_ctr += 1
                continue

            # table content
            if date_key != None:
                if time_convert:
                    info_date = convert_time(row[table_ttl[date_key]])
                else:
                    info_date = row[table_ttl[date_key]]
            else:
                info_date = 'static'

            # update feature info
            pat_id = row[table_ttl[pid_name]]
            for fn in fname:
                fval = row[table_ttl[fn]]
                self.feature_info[fn].append((pat_id, info_date, fval))
            line_ctr +=1
        f.close()
        return self.feature_info


    def get_feature_name(self, filename=None, featname=None):
        try:
            if filename == 'motor/MDS_UPDRS_Part_II__Patient_Questionnaire.csv':
                fname = ['NP2SPCH', 'NP2SALV', 'NP2SWAL', 'NP2EAT', 'NP2DRES',
                     'NP2HYGN',	'NP2HWRT',	'NP2HOBB',	'NP2TURN',	'NP2TRMR',
                     'NP2RISE',	'NP2WALK',	'NP2FREZ']

            if filename == 'motor/MDS_UPDRS_Part_III__Post_Dose_.csv':
                if None == featname:
                    fname = ['NP3SPCH',
                     'NP3FACXP',
                     'NP3RIGN',
                     'NP3RIGRU',	'NP3RIGLU',	'PN3RIGRL',	'NP3RIGLL',
                     'NP3FTAPR',    'NP3FTAPL',
                     'NP3HMOVR',	'NP3HMOVL',
                     'NP3PRSPR',	'NP3PRSPL',
                     'NP3TTAPR',	'NP3TTAPL',
                     'NP3LGAGR',	'NP3LGAGL',
                     'NP3RISNG',
                     'NP3GAIT',
                     'NP3FRZGT',
                     'NP3PSTBL',
                     'NP3POSTR',	'NP3BRADY',
                     'NP3PTRMR',	'NP3PTRML',
                     'NP3KTRMR',	'NP3KTRML',
                     'NP3RTARU',    'NP3RTALU',
                     'NP3RTARL',	'NP3RTALL',
                     'NP3RTALJ',	'NP3RTCON']
                elif 'hy' == featname:
                    fname = ['NHY']

            # if filename == 'MDS_UPDRS_Part_IV.csv':
            #     fname = ['NP4WDYSK',	'NP4DYSKI',	'NP4OFF', 'NP4FLCTI', 'NP4FLCTX',	 'NP4DYSTN']

        except ValueError:
            print ('please enter correct file name or feature name!')

        return fname

    def get_feature_range(self):
        frange = {'NP2SPCH':5, 'NP2SALV':5, 'NP2SWAL':5, 'NP2EAT':4, 'NP2DRES':5,
             'NP2HYGN':5,	'NP2HWRT':5,	'NP2HOBB':5, 'NP2TURN':5, 'NP2TRMR':5,
             'NP2RISE':5,	'NP2WALK':5,	'NP2FREZ':5,
             'NP3SPCH':5,
              'NP3FACXP':5,
              'NP3RIGN':5,
              'NP3RIGRU':5,	'NP3RIGLU':5,	'PN3RIGRL':5,	'NP3RIGLL':5,
              'NP3FTAPR':5,    'NP3FTAPL':5,
              'NP3HMOVR':5,	'NP3HMOVL':5,
              'NP3PRSPR':5,	'NP3PRSPL':5,
              'NP3TTAPR':5,	'NP3TTAPL':5,
              'NP3LGAGR':5,	'NP3LGAGL':5,
              'NP3RISNG':5,
              'NP3GAIT':5,
              'NP3FRZGT':5,
              'NP3PSTBL':5,
              'NP3POSTR':5,	'NP3BRADY':5,
              'NP3PTRMR':5,	'NP3PTRML':4,
              'NP3KTRMR':4,	'NP3KTRML':5,
              'NP3RTARU':5, 'NP3RTALU':4,
              'NP3RTARL':4,	'NP3RTALL':4,
              'NP3RTALJ':4,	'NP3RTCON':5, 'NHY':6}
        return frange
