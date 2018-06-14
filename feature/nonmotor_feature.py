# -*- coding: utf-8 -*-


import math
import numpy
import csv, codecs
import operator

from numeric import isint, isfloat
from time_converter import convert_time, convert_int



class NonMotorFeature(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        self.label_info = list()


    def load_feature(self, fname=None, featname=None):
        try:
            if fname == 'MDS UPDRS PartI':
                self.read_feature('nonmotor/MDS_UPDRS_Part_I.csv', date_key='INFODT')
                self.read_feature('nonmotor/MDS_UPDRS_Part_I__Patient_Questionnaire.csv', date_key='INFODT')
            elif fname == 'BJLO':
                self.read_feature('nonmotor/Benton_Judgment_of_Line_Orientation.csv', date_key='INFODT')
            elif fname == 'ESS':
                self.read_feature('nonmotor/Epworth_Sleepiness_Scale.csv', date_key='INFODT')
            elif fname == 'GDS':
                self.read_feature('nonmotor/Geriatric_Depression_Scale__Short_.csv', date_key='INFODT')
            elif fname == 'HVLT':
                self.read_feature('nonmotor/Hopkins_Verbal_Learning_Test1.csv', featname, date_key='INFODT')
            elif fname == 'LNS':
                self.read_feature('nonmotor/Letter_-_Number_Sequencing__PD_.csv', date_key='INFODT')
            elif fname == 'MoCA':
                self.read_feature('nonmotor/Montreal_Cognitive_Assessment__MoCA_.csv', date_key='INFODT')
            elif fname == 'QUIP':
                self.read_feature('nonmotor/QUIP_Current_Short.csv', date_key='INFODT')
            elif fname == 'RBD':
                self.read_feature('nonmotor/REM_Sleep_Disorder_Questionnaire.csv', date_key='INFODT')
            elif fname == 'SCOPA-AUT':
                self.read_feature('nonmotor/SCOPA-AUT1.csv',date_key='INFODT')
            elif fname == 'STAI':
                self.read_feature('nonmotor/State-Trait_Anxiety_Inventory.csv', date_key='INFODT')
        except ValueError:
            print('please enter correct file name!')

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
                # if "STAIAD" in fn or fn == "HVLTRT3":
                #     fval = str(int(fval) - 1)
                self.feature_info[fn].append((pat_id, info_date, fval))
            line_ctr +=1
        f.close()
        # print (self.feature_info)
        return self.feature_info


    def get_feature_name(self, filename=None, featname=None):
        try:
            if filename == 'nonmotor/MDS_UPDRS_Part_I.csv':
                fname = ['NP1COG', 'NP1HALL',	'NP1DPRS', 'NP1ANXS', 'NP1APAT',	'NP1DDS']

            if filename == 'nonmotor/MDS_UPDRS_Part_I__Patient_Questionnaire.csv':
                fname = ['NP1SLPN',	'NP1SLPD',	'NP1PAIN',	'NP1URIN',	'NP1CNST',	'NP1LTHD',	'NP1FATG']

            if filename == 'nonmotor/Benton_Judgment_of_Line_Orientation.csv':
                fname = ["BJLOT1","BJLOT2","BJLOT3","BJLOT4","BJLOT5","BJLOT6","BJLOT7","BJLOT8","BJLOT9","BJLOT10","BJLOT11",
                    "BJLOT12","BJLOT13","BJLOT14","BJLOT15","BJLOT16","BJLOT17","BJLOT18","BJLOT19","BJLOT20","BJLOT21","BJLOT22",
                    "BJLOT23","BJLOT24","BJLOT25","BJLOT26","BJLOT27","BJLOT28","BJLOT29","BJLOT30"]

            if filename == 'nonmotor/Epworth_Sleepiness_Scale.csv':
                fname = ["ESS1","ESS2","ESS3","ESS4","ESS5","ESS6","ESS7","ESS8"]

            # if filename == 'nonmotor/Geriatric_Depression_Scale__Short_.csv':
            #     fname = ["GDSSATIS","GDSDROPD","GDSEMPTY","GDSBORED","GDSGSPIR","GDSAFRAD","GDSHAPPY","GDSHLPLS","GDSHOME",
            #     "GDSMEMRY","GDSALIVE","GDSWRTLS","GDSENRGY","GDSHOPLS","GDSBETER"]

            if filename == 'nonmotor/Hopkins_Verbal_Learning_Test1.csv':
                fname = ["HVLTRT1","HVLTRT2","HVLTRT3","HVLTRDLY","HVLTREC","HVLTFPRL", "HVLTFPUN", "HVLTVRSN"]

            if filename == 'nonmotor/Letter_-_Number_Sequencing__PD_.csv':
                fname = ["LNS1A","LNS1B","LNS1C","LNS2A","LNS2B","LNS2C","LNS3A","LNS3B","LNS3C","LNS4A","LNS4B",
                "LNS4C","LNS5A","LNS5B","LNS5C","LNS6A","LNS6B","LNS6C","LNS7A","LNS7B","LNS7C"]

            if filename == 'nonmotor/Montreal_Cognitive_Assessment__MoCA_.csv':
                fname = ["MCAALTTM","MCACUBE","MCACLCKC","MCACLCKN","MCACLCKH","MCALION","MCARHINO","MCACAMEL",
                "MCAFDS","MCABDS","MCAVIGIL","MCASER7","MCASNTNC","MCAVF","MCAABSTR","MCAREC1","MCAREC2",
                "MCAREC3","MCAREC4","MCAREC5"]

            if filename == 'nonmotor/QUIP_Current_Short.csv':
                fname = ["TMGAMBLE","CNTRLGMB","TMSEX","CNTRLSEX","TMBUY","CNTRLBUY",
                "TMEAT","CNTRLEAT","TMTORACT","TMTMTACT","TMTRWD"]

            if filename == 'nonmotor/REM_Sleep_Disorder_Questionnaire.csv':
                fname = ["DRMVIVID","DRMAGRAC","DRMNOCTB","SLPLMBMV","SLPINJUR",
                "DRMVERBL","DRMFIGHT","DRMUMV","DRMOBJFL","MVAWAKEN","DRMREMEM","SLPDSTRB",
                "STROKE","HETRA","PARKISM","RLS","NARCLPSY","DEPRS","EPILEPSY","BRNINFM",
                "CNSOTH"]

            # if filename == 'nonmotor/SCOPA-AUT1.csv':
            #     fname = ["SCAU1","SCAU2","SCAU3","SCAU4","SCAU5","SCAU6","SCAU7",
            #     "SCAU8","SCAU9","SCAU10","SCAU11","SCAU12","SCAU13","SCAU14","SCAU15","SCAU16",
            #     "SCAU17","SCAU18","SCAU19","SCAU20","SCAU21","SCAU26A","SCAU26B","SCAU26C","SCAU26D"]

            # if filename == 'nonmotor/State-Trait_Anxiety_Inventory.csv':
            #     fname = ["STAIAD1","STAIAD2","STAIAD3","STAIAD4","STAIAD5","STAIAD6","STAIAD7",
            #     "STAIAD8","STAIAD9","STAIAD10","STAIAD11","STAIAD12","STAIAD13","STAIAD14",
            #     "STAIAD15","STAIAD16","STAIAD17","STAIAD18","STAIAD19","STAIAD20","STAIAD21",
            #     "STAIAD22","STAIAD23","STAIAD24","STAIAD25","STAIAD26","STAIAD27","STAIAD28",
            #     "STAIAD29","STAIAD30","STAIAD31","STAIAD32","STAIAD33","STAIAD34","STAIAD35",
            #     "STAIAD36","STAIAD37","STAIAD38","STAIAD39","STAIAD40"]

        except ValueError:
            print('please enter correct file name or feature name!')

        return fname


    def get_feature_range(self):
        frange = {'NP1COG':5,'NP1HALL':5,'NP1DPRS':5,'NP1ANXS':5,'NP1APAT':5,'NP1DDS':4,'NP1SLPN':5,'NP1SLPD':5,'NP1PAIN':5,'NP1URIN':5,'NP1CNST':5,'NP1LTHD':5,'NP1FATG':5,
            "BJLOT1":2,"BJLOT2":2,"BJLOT3":2,"BJLOT4":2,"BJLOT5":2,"BJLOT6":2,"BJLOT7":2,"BJLOT8":2,"BJLOT9":2,"BJLOT10":2,"BJLOT11":2,
            "BJLOT12":2,"BJLOT13":2,"BJLOT14":2,"BJLOT15":2,"BJLOT16":2,"BJLOT17":2,"BJLOT18":2,"BJLOT19":2,"BJLOT20":2,"BJLOT21":2,"BJLOT22":2,
            "BJLOT23":2,"BJLOT24":2,"BJLOT25":2,"BJLOT26":2,"BJLOT27":2,"BJLOT28":2,"BJLOT29":2,"BJLOT30":2,
            "ESS1":4,"ESS2":4,"ESS3":4,"ESS4":4,"ESS5":4,"ESS6":4,"ESS7":4,"ESS8":4,
            "GDSSATIS":2,"GDSDROPD":2,"GDSEMPTY":2,"GDSBORED":2,"GDSGSPIR":2,"GDSAFRAD":2,"GDSHAPPY":2,"GDSHLPLS":2,"GDSHOME":2,
            "GDSMEMRY":2,"GDSALIVE":2,"GDSWRTLS":2,"GDSENRGY":2,"GDSHOPLS":2,"GDSBETER":2,
            "HVLTRT1":13,"HVLTRT2":13,"HVLTRT3":12,"HVLTRDLY":13,"HVLTREC":13,"HVLTFPRL":9, "HVLTFPUN":10, "HVLTVRSN":7,
            "LNS1A":2,"LNS1B":2,"LNS1C":2,"LNS2A":2,"LNS2B":2,"LNS2C":2,"LNS3A":2,"LNS3B":2,"LNS3C":2,"LNS4A":2,"LNS4B":2,
            "LNS4C":2,"LNS5A":2,"LNS5B":2,"LNS5C":2,"LNS6A":2,"LNS6B":2,"LNS6C":2,"LNS7A":2,"LNS7B":2,"LNS7C":2,
            "MCAALTTM":2,"MCACUBE":2,"MCACLCKC":2,"MCACLCKN":2,"MCACLCKH":2,"MCALION":2,"MCARHINO":2,"MCACAMEL":2,
            "MCAFDS":2,"MCABDS":2,"MCAVIGIL":2,"MCASER7":4,"MCASNTNC":3,"MCAVF":2,"MCAABSTR":3,"MCAREC1":2,"MCAREC2":2,"MCAREC3":2,"MCAREC4":2,"MCAREC5":2,
            "TMGAMBLE":2,"CNTRLGMB":2,"TMSEX":2,"CNTRLSEX":2,"TMBUY":2,"CNTRLBUY":2, "TMEAT":2,"CNTRLEAT":2,"TMTORACT":2,"TMTMTACT":2,"TMTRWD":2,
            "DRMVIVID":2,"DRMAGRAC":2,"DRMNOCTB":2,"SLPLMBMV":2,"SLPINJUR":2,"DRMVERBL":2,"DRMFIGHT":2,"DRMUMV":2,"DRMOBJFL":2,"MVAWAKEN":2,"DRMREMEM":2,"SLPDSTRB":2,
            "STROKE":2,"HETRA":2,"PARKISM":2,"RLS":2,"NARCLPSY":2,"DEPRS":2,"EPILEPSY":2, "BRNINFM":2, "CNSOTH":2,
            "SCAU1":4,"SCAU2":4,"SCAU3":4,"SCAU4":4,"SCAU5":4,"SCAU6":4,"SCAU7":4,"SCAU8":5,"SCAU9":5,"SCAU10":5,"SCAU11":5,"SCAU12":5,"SCAU13":5,
            "SCAU14":4,"SCAU15":4,"SCAU16":4,"SCAU17":4,"SCAU18":4,"SCAU19":4,"SCAU20":4,"SCAU21":4,"SCAU26A":2,"SCAU26B":2,"SCAU26C":2,"SCAU26D":2,
            # "STAIAD1":4,"STAIAD2":4,"STAIAD3":4,"STAIAD4":4,"STAIAD5":4,"STAIAD6":4,"STAIAD7":4,
            # "STAIAD8":4,"STAIAD9":4,"STAIAD10":4,"STAIAD11":4,"STAIAD12":4,"STAIAD13":4,"STAIAD14":4,"STAIAD15":4,"STAIAD16":4,"STAIAD17":4,"STAIAD18":4,"STAIAD19":4,"STAIAD20":4,"STAIAD21":4,
            # "STAIAD22":4,"STAIAD23":4,"STAIAD24":4,"STAIAD25":4,"STAIAD26":4,"STAIAD27":4,"STAIAD28":4,"STAIAD29":4,"STAIAD30":4,"STAIAD31":4,"STAIAD32":4,"STAIAD33":4,"STAIAD34":4,"STAIAD35":4,
            # "STAIAD36":4,"STAIAD37":4,"STAIAD38":4,"STAIAD39":4,"STAIAD40":4
            }
        return frange
