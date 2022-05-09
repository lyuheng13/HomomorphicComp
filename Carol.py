import numpy as np
import tenseal as ts
import pandas as pd
import pickle
import datetime
from pytz import timezone
import warnings
import Public


def fetchFHEData(scheme):
    with open(Public.public_ctx_path, 'rb') as f: context = ts.context_from(pickle.load(f))
    enc_confirmed, enc_deaths = {}, {}
    with open(Public.enc_conf_path, 'rb') as f:
        read = pickle.load(f)
    for date in list(read.keys()):
        if scheme == 'CKKS':
            enc_confirmed[date] = ts.ckks_vector_from(context, read[date])
        if scheme == 'BFV':
            enc_confirmed[date] = ts.bfv_vector_from(context, read[date])

    with open(Public.enc_deaths_path, 'rb') as f:
        read = pickle.load(f)
    for date in list(read.keys()):
        if scheme == 'CKKS':
            enc_deaths[date] = ts.ckks_vector_from(context, read[date])
        if scheme == 'BFV':
            enc_deaths[date] = ts.bfv_vector_from(context, read[date])
    return enc_confirmed, enc_deaths


def CKKSEvalFunc(enc_confirmed, enc_deaths, FIPS_lookup):
    last_week_date = datetime.datetime.strftime(datetime.datetime.now(timezone('US/Eastern')) - datetime.timedelta(days=7), '%-m/%-d/%-y')

    # print('Total confirmed cases in US since 1/22/20')
    # func = (enc_confirmed[latest_record_date] - enc_confirmed['1/22/20']).sum()

    # print('Total deaths in US since 1/22/20')
    # func = (enc_deaths[latest_record_date] - enc_deaths['1/22/20']).sum()

    # print('Confirmed cases from last week (' + last_week_date + '-' + latest_record_date + ') in Queens, New York')
    # FIPSindicator = getFIPSInd(FIPS_lookup, 'Queens', 'New York')
    # func = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator)

    # print('Confirmed cases from last week (' + last_week_date + '-' + latest_record_date + ') of California and New York State')
    # FIPSindicator_cali = getFIPSInd(FIPS_lookup, State='California')
    # FIPSindicator_nys = getFIPSInd(FIPS_lookup, State='New York')
    # func_cali = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_cali)
    # func_nys = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_nys)
    # return [func_cali, func_nys]

    FIPSindicator_caliandnys = np.add(Public.getFIPSInd(FIPS_lookup, State='California'), Public.getFIPSInd(FIPS_lookup, State='New York'))
    print('Confirmed cases sum from last week (' + last_week_date + '-' + Public.latest_record_date + ') in California and New York State')
    func = (enc_confirmed[Public.latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_caliandnys)

    with open(Public.enc_result_path, 'wb') as f:
        pickle.dump(func.serialize(), f)


def BFVEvalFunc(enc_confirmed, enc_deaths, FIPS_lookup):
    last_week_date = datetime.datetime.strftime(datetime.datetime.now(timezone('US/Eastern')) - datetime.timedelta(days=7), '%-m/%-d/%-y')

    # FIPSindicator = getFIPSInd(FIPS_lookup, 'Queens', 'New York')
    # print('Confirmed cases from last week (' + last_week_date + '-' + latest_record_date + ') in Queens, New York')
    # func = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator)

    # print('Confirmed cases from last week (' + last_week_date + '-' + latest_record_date + ') of California and New York State')
    # FIPSindicator_cali = getFIPSInd(FIPS_lookup, State='California')
    # FIPSindicator_nys = getFIPSInd(FIPS_lookup, State='New York')
    # func_cali = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_cali)
    # func_nys = (enc_confirmed[latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_nys)
    # return [func_cali, func_nys]

    FIPSindicator_caliandnys = np.add(Public.getFIPSInd(FIPS_lookup, State='California'), Public.getFIPSInd(FIPS_lookup, State='New York'))
    print('Confirmed cases sum from last week (' + last_week_date + '-' + Public.latest_record_date + ') in California and New York State')
    func = (enc_confirmed[Public.latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator_caliandnys)

    with open(Public.enc_result_path, 'wb') as f:
        pickle.dump(func.serialize(), f)
