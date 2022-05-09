import numpy as np
import tenseal as ts
import pandas as pd
import pickle
import datetime
from pytz import timezone
import warnings

latest_record_date = datetime.datetime.strftime(
    datetime.datetime.now(timezone('US/Eastern')) - datetime.timedelta(days=1), '%-m/%-d/%-y')
enc_conf_path, enc_deaths_path = './enc_confirmed.pkl', './enc_deaths.pkl'
public_ctx_path = './publicContext.pkl'
enc_result_path = './result.pkl'


def getFIPSInd(FIPS_lookup, County=' ', State=' '):
    # get a indicator vector
    if County == ' ' and State == ' ':
        indicator = np.ones(FIPS_lookup.shape[0])
    if County == ' ' and State != ' ':
        indicator = (FIPS_lookup['Province_State'] == State).astype(int)
    if County != ' ' and State == ' ':
        warnings.warn('County not specified to a State, please check again.')
        indicator = np.zeros(FIPS_lookup.shape[0])
    if County != ' ' and State != ' ':
        indicator = ((FIPS_lookup['County'] == County) & (FIPS_lookup['Province_State'] == State)).astype(int)

    if FIPS_lookup['FIPS'].dot(indicator) == 0:
        warnings.warn('Wrong county or state name, please check again.')
    return indicator.tolist()


def getDates(begin_date='1/22/20', end_date=datetime.datetime.now(timezone('US/Eastern')).strftime('%D')):
    """
    default params:
    begin_date: 1/22/20, the beginning of records
    end_date: today in US/Eastern timezone
    """
    begin_date, end_date = datetime.datetime.strptime(begin_date, '%m/%d/%y'), datetime.datetime.strptime(end_date,
                                                                                                          '%m/%d/%y')
    date_list = []
    if begin_date < datetime.datetime.strptime('1/22/20', '%m/%d/%y'):
        warnings.warn('Invalid begin date, automatically changed to 1/22/20.')
        begin_date = datetime.datetime.strptime('1/22/20', '%m/%d/%y')
    if end_date.astimezone(timezone('US/Eastern')).strftime('%D') >= datetime.datetime.now(
            timezone('US/Eastern')).strftime('%D'):
        warnings.warn('Invalid end date, automatically changed to today (UTC).')
        end_date = datetime.datetime.strptime(datetime.datetime.now(timezone('US/Eastern')).strftime('%D'), '%m/%d/%y')
    while begin_date < end_date:
        date_str = str(int(begin_date.strftime('%m'))) + '/' + \
                   str(int(begin_date.strftime('%d'))) + '/' + \
                   begin_date.strftime('%y')
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list
