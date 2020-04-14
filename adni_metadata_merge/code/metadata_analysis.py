#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:02:48 2020

@author: mfromano
"""


import pandas as pd
import numpy as np
import os
os.chdir('/home/mfromano/Research/alzheimers/adni_metadata_analysis/code/')
from metadata_locations import *

# class with info for each participant
class ParticipantCollection:
    def __init__(self,user_id):
        self.user_id = user_id
        self.registry = data_from_user(user_id, REGISTRY_LOC, 'reg',reg_fields)
        self.tau = pd.concat([data_from_user(user_id,TAUMETA2_LOC,'tau',tau2_fields), \
                                     data_from_user(user_id, TAUMETA3_LOC,'tau',tau2_fields)])
        self.pib = data_from_user(user_id,PIBMETA_LOC,'pib',pib_fields)
        self.mri1 = data_from_user(user_id,MRI1META_LOC,'mri',mri1_fields)
        self.mri3 = data_from_user(user_id,MRI3META_LOC,'mri',mri3_fields)
        self.MMSE = data_from_user(user_id,MMSE_LOC,'mmse',mmse_fields)
        self.NPIQ = data_from_user(user_id,NPIQ_LOC,'npiq',npiq_fields)
        self.NPI = data_from_user(user_id, NPI_LOC,'npi',npi_fields)
        self.NEUROBAT = data_from_user(user_id, NEUROBAT_LOC,'neurobat',nb_fields)
        self.MOCA = data_from_user(user_id, MOCA_LOC,'moca',moca_fields)
        self.CDR = data_from_user(user_id, CDR_LOC,'cdr',cdf_fields)
        # self.merge_data()
        
    def merge_data(self):
        #identify unique visits and dates for patients
        phase = self.registry.Phase.to_numpy()
        visits2 = self.registry.VISCODE2.to_numpy()
        visits1 = self.registry.VISCODE.to_numpy()
        assert(len(visits1) == len(visits2))
        examdates = self.registry.EXAMDATE.to_numpy()
        #for each unique visit, query: MRI weight? Tau? Pib? MMSE? NPIQ? NPI? NeuroBat? MOCA? CDR? 
        column_headers = ['Phase','RID','VISCODE1','VISCODE2',\
            'DATE','MRI1','MRI3',\
             'Tau','PIB','MMSE',\
             'NPIQ','NPI',\
              'NeuroBat','MOCA','CDR']
        self.output_table = pd.DataFrame(data=None,\
            columns=column_headers)
        for i in range(len(visits1)):
            visit_data = self.data_from_visitid(phase[i], visits1[i], visits2[i], examdates[i])
            self.output_table = self.output_table.append(pd.DataFrame(data = [visit_data], columns = column_headers), ignore_index=True)
            
    def data_from_visitid(self, phase, visit1, visit2,examdate):
        
        all_data = [phase, self.user_id, visit1, visit2, examdate]
        
        def add_columns(field, all_data, hasfield_val = None):
            if len(field) == 0:
                all_data = all_data + [0]
                return all_data
            
            if 'VISCODE2' in field.columns and not pd.isnull(visit2):
                field_entries = field.loc[(field.VISCODE2.eq(visit2)) & \
                    (field.Phase.eq(phase))]
            else:
                field_entries = field.loc[field.VISCODE.eq(visit1)]
            
            # if the given assessment can't be located for a field, set it as 0
            if len(field_entries) == 0:
                all_data = all_data + [0]
            # otherwise, if there is an entry for the field but no 
            #indicator as to whether or not it was performed, set it as a 1
            elif hasfield_val is None:
                all_data = all_data + [1]
            # otherwise, if there is an entry for the field and an indicator
            # get the value of the indicator
            elif hasfield_val is not None:
                value_to_add = pd.to_numeric(getattr(field_entries, hasfield_val)).values
                # if any of the values are equal to 1, set to 1
                if any(value_to_add == 1):
                    all_data = all_data + [1]
                # otherwise, if they are all equal to 0, set as 0
                elif all(value_to_add == 0):
                    all_data = all_data + [0]
                else:
                    all_data = all_data + [-4]
            else:
                error('undefined condition')
            return all_data

        all_data = add_columns(self.mri1, all_data, 'MMCONDCT')
        all_data = add_columns(self.mri3, all_data, 'MMCONDCT')
        all_data = add_columns(self.tau, all_data, 'DONE')
        all_data = add_columns(self.pib, all_data, 'PBCONDCT')
        all_data = add_columns(self.MMSE, all_data)
        all_data = add_columns(self.NPIQ, all_data)
        all_data = add_columns(self.NPI, all_data)
        all_data = add_columns(self.NEUROBAT, all_data)
        all_data = add_columns(self.MOCA, all_data)
        all_data = add_columns(self.CDR, all_data)
        return all_data
            
def parse_field(df, columns):
    parsed_table = pd.DataFrame(data = [df[col] for col in columns]).T
    return parsed_table
    
def data_from_user(user_id,fi,label,fields):
    data_fi = pd.read_csv(fi)
    locs = data_fi.RID.loc[data_fi.RID == user_id]
    table_entries = data_fi.loc[locs.index]
    fields = parse_field(table_entries,fields)
    fields['Exam'] = pd.Series(np.repeat(label,len(fields)),index = fields.index)
    if 'PHASE' in fields.columns:
        fields = fields.rename(columns={'PHASE': 'Phase'})
    return fields


# want output table: RID, visit, MRI? Weight? Tau? Pib? MMSE? NPIQ? NPI? NeuroBat? MOCA? CDR?
def test():
    a = ParticipantCollection(677)
    return(a)

# if __name__ == '__main__':

tau_sheet = pd.read_csv(TAUMETA2_LOC)
tau_sheet3 = pd.read_csv(TAUMETA3_LOC)

tau_subjects = np.union1d(pd.unique(tau_sheet.RID),pd.unique(tau_sheet3.RID))

# get info across all 5 documents for all subjects
participants_tau = [ParticipantCollection(x) for x in tau_subjects]
print('finished generating participants')
for x in participants_tau:
    x.merge_data()
output_collection = [x.output_table for x in participants_tau]
output_spreadsheet = pd.concat(output_collection)
data_output = output_spreadsheet.to_csv('summary_metadata.csv')