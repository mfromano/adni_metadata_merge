#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:02:48 2020

@author: mfromano
"""


import pandas as pd
import numpy as np
import os
os.chdir('/home/mfromano/Research/alzheimers/adni_metadata_merge/code/')
from metadata_locations import *

# FILE_LIST = {'tau2': tau2, 'tau3': tau3, 'mri1': mri1, 'mri3': mri3, 'pib': pib,\
#              'mmse': mmse, 'npiq': npiq, 'npi':npi,'nb':nb, 'moca':moca, 'cdf': cdf,\
#                  'reg': reg, 'dxsum': dxsum, 'arm': arm}

'''
    This class takes as input a unique user identifier and generates attributes
    consisting of dataframes for each csv in file_list
'''
# class with info for each participant
class ParticipantCollection:
    def __init__(self,user_id):
        self.user_id = user_id
        for key in FILE_LIST.keys():
            setattr(self,key,data_from_user(user_id, FILE_LIST[key]['loc'], FILE_LIST[key]['fields']))


'''
    This function takes a dataframe and specified columns. returns a dataframe
    consisting of the data contained within those columns
'''
def parse_field(df, columns):
    parsed_table = pd.DataFrame(data = [df[col] for col in columns]).T
    return parsed_table

'''
     This function takes a user ID, a file location, and the fields to look for
     in the CSV file. It returns a dataframe consisting of only those columns.
     It also renames 
'''
def data_from_user(user_id,fi,fields):
    data_fi = pd.read_csv(fi)
    locs = data_fi.RID.loc[data_fi.RID == user_id] # find entries that match RID
    table_entries = data_fi.loc[locs.index] #get the entire rows
    fields = parse_field(table_entries,fields) #get the values for all of the desired fields
    if 'PHASE' in fields.columns: #homogenize the 'Phase' column
        fields = fields.rename(columns={'PHASE': 'Phase'})
    return fields

'''
    This function takes as input a ParticipantCollection object and asks whether
    or not, for each unique visit, there exists a datapoint for each of the csv
    files.
    
    Unique identifiers for each visit REQUIRE an identical match between:
        Phase, VISCODE, and VISCODE2
'''
def merge_data(pc):
    
    # convert these to numpy arrays
    unique_ids = pc.reg[['Phase', 'RID', 'VISCODE', 'VISCODE2', 'EXAMDATE']]

    #for each unique visit, query: MRI weight? Tau? Pib? MMSE? NPIQ? NPI? NeuroBat? MOCA? CDR? 
    column_headers = ['Phase','RID','VISCODE1','VISCODE2','DATE','DX']
    
    #add as column headers all of the csv sheets that are assessments
    exam_headers = []
    for key in FILE_LIST.keys():
        if FILE_LIST[key]['isexam'] == 1:
            exam_headers.append(key)
            column_headers.append(key)
    #initialize output table
    output_table = pd.DataFrame(data=None,\
        columns=column_headers)
    
    for index, unique_id in unique_ids.iterrows():
        visit_data = data_from_visitid(pc, unique_id)
        output_table = output_table.append(pd.DataFrame(data = [visit_data], columns = column_headers), ignore_index=True)
        
    return output_table


'''
    Given a ParticipantCollection, identifiers for a particular visit,and csv keys
    return a summary row with information from each of the CSVs included in
'''
def data_from_visitid(pc, unique_id):
    all_data = unique_id.values.tolist()
    visit1 = unique_id.VISCODE
    visit2 = unique_id.VISCODE2
    phase = unique_id.Phase
    
    def add_columns(exam_csv, all_data, hasfield_val = None):

        # get entry from csv corresponding to the unique identifier
        exam_entry = get_exam_entry(exam_csv)

        # if the given assessment can't be located for a field, set it as 0
        if len(exam_entry) == 0:
            all_data = all_data + [0]
        
        # otherwise, if there is an entry for the field but no 
        #indicator as to whether or not it was performed, set it as a 1
        elif (len(exam_entry) > 0) and (hasfield_val is None):
            all_data = all_data + [1]
            
        # otherwise, if there is an entry for the field and an indicator
        # get the value of the indicator
        elif hasfield_val is not None:
            value_to_add = pd.to_numeric(getattr(exam_entry, hasfield_val)).values
            # if any of the values are equal to 1, set to 1
            if any(value_to_add == 1):
                all_data = all_data + [1]
            # otherwise, if they are all equal to 0, set as 0
            elif all(value_to_add == 0):
                all_data = all_data + [0]
            else:
                all_data = all_data + [-4]
        else:
            raise TypeError('undefined condition')
        return all_data

    '''
        Given an exam csv for a particular patient, identify the data for
        the given exam
    '''
    def get_exam_entry(exam_csv):
        if 'VISCODE2' in exam_csv.columns and not pd.isnull(visit2):
            exam_entry = exam_csv.loc[(exam_csv.VISCODE2.eq(visit2)) & \
                (exam_csv.Phase.eq(phase)) & exam_csv.VISCODE.eq(visit1)]
        elif 'Phase' in exam_csv.columns:
            exam_entry = exam_csv.loc[(exam_csv.VISCODE.eq(visit1)) &\
                                      (exam_csv.Phase.eq(phase))]
        else:
            exam_entry = exam_csv.loc[(exam_csv.VISCODE.eq(visit1))] 
        return exam_entry

        
    '''    
        Given a subject's arm and dxsum csv's, add value that corresponds to
        the patient's diagnosis
    '''
    def add_dx_columns(arm, dxsum, all_data):
        
        # if the phase is ADNI1, 2, or GO, and this is a screening exam, 
        # find the screening diagnosis in the arm csv
        if (phase != 'ADNI3') and ((pd.isnull(visit2) and visit1 == 'sc') or (visit2 == 'sc')):
            
            # get the dx code 
            cur_arm = arm.loc[arm.Phase == phase]
            if len(cur_arm) != 1:
                print('More than 1 arm value')
                raise
            dx_code = cur_arm.ARM
            
            #convert dx code into a diagnosis
            converted_value = DX_TRANS['ARM'][phase][int(dx_code)]
            
        #if the phase ADNI3, or this is not an 'sc' visit
        else:
            # get entry in dxsum
            entry_row = get_exam_entry(dxsum)
            
            # find the field corresponding to the phase of the trial
            if phase == 'ADNI1':
                entry_value = entry_row.DXCURREN
            elif (phase == 'ADNI2') or (phase == 'ADNIGO'):
                entry_value = entry_row.DXCHANGE
            elif phase == 'ADNI3':
                entry_value = entry_row.DIAGNOSIS
            else:
                print('Invalid phase entered!')
                raise
            
            # determine the converted value
            if len(entry_value) == 1:
                if entry_value.isnull().bool():
                    converted_value = -4
                else:
                    converted_value = DX_TRANS[str(phase)][int(entry_value)]
            elif len(entry_value) == 0:
                converted_value = -4
            else:
                raise TypeError('more than 1 diagnosis code for this visit')
                
        
        all_data = all_data + [converted_value]
        return all_data
    
    all_data = add_dx_columns(pc.arm, pc.dxsum, all_data)
    
    for key in FILE_LIST.keys():
        if FILE_LIST[key]['isexam'] == 1:
            if FILE_LIST[key]['isimage'] == 1:
                all_data = add_columns(getattr(pc,key), all_data, FILE_LIST[key]['DONECOL'])
            else:
                all_data = add_columns(getattr(pc,key), all_data)
    
    return all_data

tau_sheet = pd.read_csv(TAUMETA2_LOC)
tau_sheet3 = pd.read_csv(TAUMETA3_LOC)

tau_subjects = np.union1d(pd.unique(tau_sheet.RID),pd.unique(tau_sheet3.RID))

# get info across all 5 documents for all subjects
participants_tau = [ParticipantCollection(x) for x in tau_subjects]
print('finished generating participants')
output_collection = []
for x in participants_tau:
    output_collection.append(merge_data(x))
output_spreadsheet = pd.concat(output_collection)
output_spreadsheet.to_csv('summary_metadata.csv')
