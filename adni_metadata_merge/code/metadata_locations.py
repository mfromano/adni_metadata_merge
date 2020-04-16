#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 15:04:13 2020

@author: mfromano
"""


# hard-code csv's w/ metadata
BASE_DIR = '/home/mfromano/Research/alzheimers/data/'

# PET scans
TAUMETA2_LOC = BASE_DIR + 'TAUMETA.csv'
tau2_fields = ['Phase','RID','VISCODE','VISCODE2', 'DONE', 'SCANDATE']
tau2 = {'loc': TAUMETA2_LOC, 'fields': tau2_fields, 'isexam':1, 'isimage': 1, 'DONECOL': 'DONE'}

TAUMETA3_LOC = BASE_DIR + 'TAUMETA3.csv'
tau3_fields = ['Phase','RID','VISCODE','VISCODE2', 'DONE', 'SCANDATE']
tau3 = {'loc': TAUMETA3_LOC, 'fields': tau3_fields, 'isexam':1, 'isimage': 1, 'DONECOL': 'DONE'}

PIBMETA_LOC = BASE_DIR + 'PIBMETA.csv'
pib_fields = ['RID', 'VISCODE', 'EXAMDATE', 'PBCONDCT'] #PBCONDCT = 0 = no scan conducted
pib = {'loc': PIBMETA_LOC, 'fields': pib_fields, 'isexam':1,'isimage': 1, 'DONECOL': 'PBCONDCT'}

# MRI
MRI1META_LOC = BASE_DIR + 'MRI1pt5META.csv'
mri1_fields = ['PHASE', 'FIELD_STRENGTH', 'RID', 'VISCODE','VISCODE2', 'MMCONDCT', 'MMREASON','EXAMDATE']
mri1 = {'loc': MRI1META_LOC, 'fields': mri1_fields, 'isexam':1,'isimage': 1, 'DONECOL': 'MMCONDCT'}

MRI3META_LOC = BASE_DIR + 'MRI3META.csv'
mri3_fields = ['PHASE', 'FIELD_STRENGTH', 'RID', 'VISCODE', 'VISCODE2', 'MMCONDCT', 'MMREASON','EXAMDATE']
mri3 = {'loc': MRI3META_LOC, 'fields': mri3_fields,'isexam':1, 'isimage': 1, 'DONECOL': 'MMCONDCT'}

#Psych test logs
MMSE_LOC = BASE_DIR + 'MMSE.csv'
mmse_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']
mmse = {'loc': MMSE_LOC, 'fields': mmse_fields, 'isexam':1,'isimage': 0}

NPIQ_LOC = BASE_DIR + 'NPIQ.csv'
npiq_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']
npiq = {'loc': NPIQ_LOC, 'fields': npiq_fields, 'isexam':1,'isimage': 0}

NPI_LOC = BASE_DIR + 'NPI.csv'
npi_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']
npi = {'loc': NPI_LOC, 'fields': npi_fields, 'isexam':1,'isimage': 0}

NEUROBAT_LOC = BASE_DIR + 'NEUROBAT.csv'
nb_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE'] #Note: missing data in clockcirc, clocksym, etc. for many of these
nb = {'loc': NEUROBAT_LOC, 'fields': nb_fields, 'isexam':1,'isimage': 0}

MOCA_LOC = BASE_DIR + 'MOCA.csv' # note: there is no "examdate" or equivalent here. Have to use surrogate
moca_fields = ['Phase','RID','VISCODE', 'VISCODE2']
moca = {'loc': MOCA_LOC, 'fields': moca_fields, 'isexam':1,'isimage': 0}

CDR_LOC = BASE_DIR + 'CDR.csv'
cdr_fields = ['Phase', 'RID', 'VISCODE','VISCODE2', 'EXAMDATE']
cdr = {'loc': CDR_LOC, 'fields': cdr_fields, 'isexam':1,'isimage': 0}

REGISTRY_LOC = BASE_DIR + 'REGISTRY.csv'
reg_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']
reg = {'loc': REGISTRY_LOC, 'fields': reg_fields,'isexam':0, 'isimage': 0}

# ADNI_MERGE_LOC = BASE_DIR + 'ADNIMERGE.csv'
# merge_fields = ['Phase','RID','PTID','VISCODE','COLPROT','ORIGPROT','EXAMDATE','DX_bl','AGE','APOE4']
# merge = {'loc': ADNI_MERGE_LOC, 'fields': merge_fields}

#coding for "DIAGNOSIS" (ADNI3)
#1=CN	2=MCI	3=Dementia
#coding for DXCURREN (ADNI1)
#1=NL	2=MCI	3=AD
#coding for dxchange (ADNI2/GO):
#1=Stable: NL to NL	 2=Stable: MCI to MCI	 3=Stable: Dementia to Dementia
# 4=Conversion: NL to MCI	 5=Conversion: MCI to Dementia	 
#6=Conversion: NL to Dementia	 7=Reversion: MCI to NL	 8=Reversion: Dementia to MCI
#9=Reversion: Dementia to NL

DX_SUM_LOC = BASE_DIR + 'DX_SUM_ALL.csv'
dxsum_fields = ['Phase','RID','VISCODE','VISCODE2','EXAMDATE','DXCHANGE','DXCURREN','DIAGNOSIS'] # finish this
dxsum = {'loc': DX_SUM_LOC, 'fields': dxsum_fields, 'isexam':0, 'isimage':0}

#coding for "ARM"
#1=NL - 1.5T only	2=MCI - 1.5T only	3=AD - 1.5T only	4=NL - PET+1.5T	5=MCI - PET+1.5T	6=AD - PET+1.5T	7=NL - 3T+1.5T	8=MCI - 3T+1.5T	9=AD - 3T+1.5T
ARM_LOC = BASE_DIR + 'ARM.csv'
arm_fields = ['Phase','RID','ARM']
arm = {'loc': ARM_LOC, 'fields': arm_fields, 'isexam':0 , 'isimage':0}


FILE_LIST = {'tau2': tau2, 'tau3': tau3, 'mri1': mri1, 'mri3': mri3, 'pib': pib,\
             'mmse': mmse, 'npiq': npiq, 'npi':npi,'nb':nb, 'moca':moca, 'cdr': cdr,\
                 'reg': reg, 'dxsum': dxsum, 'arm': arm}
    

# Now define the mappings from number to cognitive deficit
ADNI3_TRANS = {1: 'CN',2: 'MCI', 3: 'AD'}
ADNI1_TRANS = {1: 'NL',2: 'MCI', 3: 'AD'}
ADNI2GO_TRANS = {1: 'NL',2: 'MCI', 3: 'AD', 4: 'MCI', 5: 'AD', 6: 'AD', 7: 'NL', 8: 'MCI', 9: 'NL'}


ARM_ADNI2_TRANS = {1: 'NL',2: 'MCI', 3: 'AD', 4: 'NL', 5: 'MCI', 6: 'AD', 7: 'NL', 8: 'LMCI', 9: 'AD', 10:'EMCI',11:'SMC'}
ARM_ADNIGO_TRANS = {1: 'NL',2: 'MCI', 3: 'AD', 4: 'NL', 5: 'MCI', 6: 'AD', 7: 'NL', 8: 'MCI', 9: 'AD', 10: 'EMCI'}
ARM_ADNI1_TRANS = {1: 'NL',2: 'MCI', 3: 'AD', 4: 'NL', 5: 'MCI', 6: 'AD', 7: 'NL', 8: 'MCI', 9: 'AD'}

DX_TRANS = {'ADNI1': ADNI1_TRANS, 'ADNI2': ADNI2GO_TRANS,\
            'ADNIGO': ADNI2GO_TRANS, 'ADNI3': ADNI3_TRANS,\
            'ARM': {'ADNI1': ARM_ADNI1_TRANS, 'ADNI2': ARM_ADNI2_TRANS, 'ADNIGO': ARM_ADNIGO_TRANS}}
