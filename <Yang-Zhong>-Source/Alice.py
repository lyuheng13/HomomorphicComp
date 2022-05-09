import numpy as np
import tenseal as ts
import pandas as pd
import pickle
import datetime
from pytz import timezone
import warnings
import Public

secret_ctx_path = './secretContext.pkl'


def CKKSSetup():
    # setup CKKS context
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.generate_galois_keys()
    context.global_scale = 2 ** 40

    secret_ckks_ctx = context.serialize(save_secret_key=True)
    with open(secret_ctx_path, 'wb') as f: pickle.dump(secret_ckks_ctx, f)
    context.make_context_public()  # drop the secret_key from the context
    public_ckks_ctx = context.serialize()
    with open(Public.public_ctx_path, 'wb') as f: pickle.dump(public_ckks_ctx, f)


def BFVSetup():
    # setup BFV context
    context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=8192, plain_modulus=1032193)
    context.generate_galois_keys()

    secret_bfv_ctx = context.serialize(save_secret_key=True)
    with open(secret_ctx_path, 'wb') as f: pickle.dump(secret_bfv_ctx, f)
    context.make_context_public()  # drop the secret_key from the context
    public_bfv_ctx = context.serialize()
    with open(Public.public_ctx_path, 'wb') as f: pickle.dump(public_bfv_ctx, f)

def dataProcess(scheme):
    # load data set
    confirmed_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv').dropna()
    deaths_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv').dropna()
    date_list = Public.getDates()

    FIPS_lookup = pd.concat(
        [confirmed_df['FIPS'].astype(int), confirmed_df['Admin2'], confirmed_df['Province_State']], axis=1).rename(
        {'Admin2': 'County'}, axis=1)
    confirmed_df = pd.concat([confirmed_df['FIPS'].astype(int), confirmed_df[date_list]], axis=1)
    deaths_df = pd.concat([deaths_df['FIPS'].astype(int), deaths_df[date_list]], axis=1)

    # FHE for data set
    with open(secret_ctx_path, 'rb') as f:
        context = ts.context_from(pickle.load(f))
    if scheme == 'CKKS':
        enc_confirmed, enc_deaths = {}, {}
        for date in date_list:
            enc_confirmed[date] = ts.ckks_vector(context, list(confirmed_df[date]))
            enc_deaths[date] = ts.ckks_vector(context, list(deaths_df[date]))

    if scheme == 'BFV':
        enc_confirmed, enc_deaths = {}, {}
        for date in date_list:
            enc_confirmed[date] = ts.bfv_vector(context, list(confirmed_df[date]))
            enc_deaths[date] = ts.bfv_vector(context, list(deaths_df[date]))

    # Store enc data
    dict_helper = {}
    for date in date_list:
        dict_helper[date] = enc_confirmed[date].serialize()
    with open(Public.enc_conf_path, 'wb') as f:
        pickle.dump(dict_helper, f)

    dict_helper = {}
    for date in date_list:
        dict_helper[date] = enc_deaths[date].serialize()
    with open(Public.enc_deaths_path, 'wb') as f:
        pickle.dump(dict_helper, f)
    return FIPS_lookup


def decrypt(scheme):
    with open(secret_ctx_path, 'rb') as f:
        context = ts.context_from(pickle.load(f))
    with open(Public.enc_result_path, 'rb') as f:
        if scheme == 'CKKS':
            enc_result = ts.ckks_vector_from(context, pickle.load(f))
        if scheme == 'BFV':
            enc_result = ts.bfv_vector_from(context, pickle.load(f))
    result = abs(round(enc_result.decrypt()[0]))
    print(scheme, 'result:', result)
