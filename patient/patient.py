# -*- coding: utf-8 -*-

class Patient(object):

   def __init__(self):
       # all other non-demographic features
       self.patient_rec = dict() # time: feature value (list or array)
       self.patient_hy = dict() # time: hy_stage
       self.patient_mci = dict() # time: mci_score
