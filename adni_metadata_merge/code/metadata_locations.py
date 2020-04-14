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

TAUMETA3_LOC = BASE_DIR + 'TAUMETA3.csv'
tau3_fields = ['Phase','RID','VISCODE','VISCODE2', 'DONE', 'SCANDATE']

PIBMETA_LOC = BASE_DIR + 'PIBMETA.csv'
pib_fields = ['RID', 'VISCODE', 'EXAMDATE', 'PBCONDCT'] #PBCONDCT = 0 = no scan conducted

# MRI
MRI1META_LOC = BASE_DIR + 'MRI1pt5META.csv'
mri1_fields = ['PHASE', 'FIELD_STRENGTH', 'RID', 'VISCODE','VISCODE2', 'MMCONDCT', 'MMREASON','EXAMDATE']

MRI3META_LOC = BASE_DIR + 'MRI3META.csv'
mri3_fields = ['PHASE', 'FIELD_STRENGTH', 'RID', 'VISCODE', 'VISCODE2', 'MMCONDCT', 'MMREASON','EXAMDATE']

#Psych test logs
MMSE_LOC = BASE_DIR + 'MMSE.csv'
mmse_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']

NPIQ_LOC = BASE_DIR + 'NPIQ.csv'
npiq_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']

NPI_LOC = BASE_DIR + 'NPI.csv'
npi_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']

NEUROBAT_LOC = BASE_DIR + 'NEUROBAT.csv'
nb_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE'] #Note: missing data in clockcirc, clocksym, etc. for many of these

MOCA_LOC = BASE_DIR + 'MOCA.csv' # note: there is no "examdate" or equivalent here. Have to use surrogate
moca_fields = ['Phase','RID','VISCODE', 'VISCODE2']

CDR_LOC = BASE_DIR + 'CDR.csv'
cdf_fields = ['Phase', 'RID', 'VISCODE','VISCODE2', 'EXAMDATE']

REGISTRY_LOC = BASE_DIR + 'REGISTRY.csv'
reg_fields = ['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']

ADNI_MERGE_LOC = BASE_DIR + 'ADNIMERGE.csv'
merge_fields = ['Phase','RID','PTID','VISCODE','COLPROT','ORIGPROT','EXAMDATE','DX_bl','AGE','APOE4']

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

#coding for "ARM"
#1=NL - 1.5T only	2=MCI - 1.5T only	3=AD - 1.5T only	4=NL - PET+1.5T	5=MCI - PET+1.5T	6=AD - PET+1.5T	7=NL - 3T+1.5T	8=MCI - 3T+1.5T	9=AD - 3T+1.5T
ARM_LOC = BASE_DIR + 'ARM.csv'
arm_fields = ['Phase','RID','ARM']
