#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:02:48 2020

@author: mfromano
"""


import pandas as pd
import warnings
import os
os.chdir('/home/mfromano/Research/alzheimers/adni_metadata_merge/code/')
from metadata_locations import FILE_LIST, DX_TRANS

"""
FILE_LIST = {'tau2': tau2, 'tau3': tau3, 'mri1': mri1, 'mri3': mri3, 'pib': pib,\
             'mmse': mmse, 'npiq': npiq, 'npi':npi,'nb':nb, 'moca':moca, 'cdf': cdf,\
                 'reg': reg, 'dxsum': dxsum, 'arm': arm}
"""



class ParticipantCollection:
    """
    This class takes as input a unique user identifier and generates attributes
    consisting of dataframes for each csv in file_list
    """
    def __init__(self,user_id):
        self.user_id = user_id
        for key in FILE_LIST.keys():
            setattr(self,key,data_from_user(user_id, FILE_LIST[key]['loc'], FILE_LIST[key]['fields']))



def parse_field(df, columns):
    """
    This function takes a dataframe and specified columns. returns a dataframe
    consisting of the data contained within those columns
    """
    parsed_table = pd.DataFrame(data = [df[col] for col in columns]).T
    return parsed_table


def data_from_user(user_id,fi,fields):
    """
     This function takes a user ID, a file location, and the fields to look for
     in the CSV file. It returns a dataframe consisting of only those columns.
     """
    data_fi = pd.read_csv(fi)
    locs = data_fi.RID.loc[data_fi.RID == user_id] # find entries that match RID
    table_entries = data_fi.loc[locs.index] #get the entire rows
    fields = parse_field(table_entries,fields) #get the values for all of the desired fields
    if 'PHASE' in fields.columns: #homogenize the 'Phase' column
        fields = fields.rename(columns={'PHASE': 'Phase'})
    return fields


def merge_data(pc):
    """
    This function takes as input a ParticipantCollection object and asks whether
    or not, for each unique visit, there exists a datapoint for each of the csv
    files.
    
    Unique identifiers for each visit REQUIRE an identical match between:
        Phase, VISCODE, and VISCODE2
    """
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


def data_from_visitid(pc, unique_id):
    """
    Given a ParticipantCollection and identifiers for a particular visit,
    return a summary row with boolean from each of the CSVs included in
    """
    summ_data = unique_id.values.tolist() 
    summ_data = add_dx_columns(pc.arm, pc.dxsum, unique_id, summ_data)
    for key in FILE_LIST.keys():
        if FILE_LIST[key]['isexam'] == 1:
            if FILE_LIST[key]['isimage'] == 1:
                summ_data = add_columns(getattr(pc,key), summ_data, unique_id, FILE_LIST[key]['DONECOL'])
            else:
                summ_data = add_columns(getattr(pc,key), summ_data, unique_id)
    return summ_data


def add_dx_columns(arm_by_rid, dxsum_by_rid, unique_id, summ_data):
    """    
    Given a subject's arm and dxsum csv's, as well as the unique identifier for
    a visit, add value that corresponds to the patient's diagnosis
    """
    visit1 = unique_id.VISCODE
    visit2 = unique_id.VISCODE2
    phase = unique_id.Phase  
    # if the phase is ADNI1, 2, or GO, and this is a screening exam, 
    # find the screening diagnosis in the arm csv
    if (phase != 'ADNI3') and ((pd.isnull(visit2) and visit1 == 'sc') or (visit2 == 'sc')):
        # get the dx code 
        converted_value = get_arm_dx(arm_by_rid, phase)
    # if the phase ADNI3, or this is not an 'sc' visit
    else:
        converted_value = get_dxsum_dx(dxsum_by_rid, unique_id)
    summ_data = summ_data + [converted_value]
    return summ_data


# get entry in dxsum
def get_dxsum_dx(dxsum_by_rid, unique_id):
    """
    Takes as arguments rows from DXSUM for a given RID, and the unique_id 
    """
    entry_row = get_exam_entry(dxsum_by_rid, unique_id)
    # find the field corresponding to the phase of the trial
    entry_value = dx_entry_from_phase(entry_row, unique_id.Phase)
    # determine the converted value
    if len(entry_value) == 1:
        if entry_value.isnull().bool():
            converted_value = -4
        else:
            converted_value = DX_TRANS[str(unique_id.Phase)][int(entry_value)]
    elif len(entry_value) == 0:
        converted_value = -4
    else:
        raise TypeError('more than 1 diagnosis code for this visit')
    return converted_value



def get_arm_dx(arm_by_rid, phase):
    """
    Given the phase and an arm csv collection of rows for a particular RID,
    return the dx value
    """
    cur_arm = arm_by_rid.loc[arm_by_rid.Phase == phase]
    dx_code = cur_arm.ARM
    if len(dx_code) == 0:
        converted_value = -4
        warnings.warn('No diagnosis code for screening visit! User: {}'.format(arm_by_rid.RID))
    else:
        # convert dx code into a diagnosis
        converted_value = DX_TRANS['ARM'][phase][int(dx_code)]
    return converted_value


def add_columns(exam_csv, summ_data, unique_id, done_column = None):
    """
    Given an exam csv for a particular exam, budding row of data, a unique
    event identifier unique_id, and the title of a column (if present) that
    confirms whether or not a study was performed, add the relevant entry for
    the study
    """
    # get entry from csv corresponding to the unique identifier
    exam_entry = get_exam_entry(exam_csv, unique_id)
    # if the given assessment can't be located for a field, set it as 0
    if len(exam_entry) == 0:
        summ_data = summ_data + [0]
    # otherwise, if there is an entry for the field but no
    # indicator as to whether or not it was performed, set it as a 1
    elif (len(exam_entry) > 0) and (done_column is None):
        summ_data = summ_data + [1]
    # otherwise, if there is an entry for the field and an indicator
    # get the value of the indicator
    elif done_column is not None:
        summ_data = add_image_bool(exam_entry, done_column, summ_data)
    else:
        raise TypeError('undefined condition')
    return summ_data



def get_exam_entry(exam_csv_by_rid, unique_id):
    """
    Given an exam csv for a particular patient, identify the data for
    the given exam given a unique identifier containing Phase, VISCODE, and
    VISCODE2
    """
    visit1 = unique_id.VISCODE
    visit2 = unique_id.VISCODE2
    phase = unique_id.Phase
    # if possible, identify based on all three criterion
    if 'VISCODE2' in exam_csv_by_rid.columns and not pd.isnull(visit2):
        exam_entry = exam_csv_by_rid.loc[(exam_csv_by_rid.VISCODE2.eq(visit2)) & \
            (exam_csv_by_rid.Phase.eq(phase)) & exam_csv_by_rid.VISCODE.eq(visit1)]
    # if VISCODE2 is missing (for example, PIB table)
    elif 'Phase' in exam_csv_by_rid.columns:
        exam_entry = exam_csv_by_rid.loc[(exam_csv_by_rid.VISCODE.eq(visit1))\
                                  & (exam_csv_by_rid.Phase.eq(phase))]
    # if both VISCODE2 and Phase are missing (for example, PIB table)
    else:
        exam_entry = exam_csv_by_rid.loc[(exam_csv_by_rid.VISCODE.eq(visit1))]
    return exam_entry


def add_image_bool(exam_entry, done_column, summ_data):
    """
    given an exam entry row, the column that determines whether or not the
    image was collected, and a list, append a value to the list that
    corresponds to whether or not the exam was done. 1 = at least one exam
    completed, 0 = no exam completed, -4 = missing data
    """
    value_to_add = pd.to_numeric(getattr(exam_entry, done_column)).values
    # if any of the values are equal to 1, set to 1
    if any(value_to_add == 1):
        summ_data = summ_data + [1]
    # otherwise, if they are all equal to 0, set as 0
    elif all(value_to_add == 0):
        summ_data = summ_data + [0]
    else:
        summ_data = summ_data + [-4]
    return summ_data


def dx_entry_from_phase(entry_row, phase):
    """
    Given a presumptive row from the DX sheet and the phase, return a
    diagnosis code. The entry row may be empty, this function does not do
    validation
    """
    if phase == 'ADNI1':
        entry_value = entry_row.DXCURREN
    elif (phase == 'ADNI2') or (phase == 'ADNIGO'):
        entry_value = entry_row.DXCHANGE
    elif phase == 'ADNI3':
        entry_value = entry_row.DIAGNOSIS
    else:
        raise ValueError('Invalid phase entered!')
    return entry_value
