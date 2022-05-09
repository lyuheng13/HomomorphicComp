# For more queries, please see EvalFunc in Carol.py,
# uncomment those functions to see the one-time result.

# This is just a demo showing how we can deal with
# multiple functions over once FHEed data to save time.

import Public
import Alice
import Carol
import numpy as np
import tenseal as ts
import pandas as pd
import pickle
import datetime
from pytz import timezone
import warnings


def BFVEvalFunc1(enc_confirmed, enc_deaths, FIPS_lookup):
    last_week_date = datetime.datetime.strftime(
        datetime.datetime.now(timezone('US/Eastern')) - datetime.timedelta(days=7), '%-m/%-d/%-y')
    FIPSindicator = Public.getFIPSInd(FIPS_lookup, State='California')
    func = (enc_confirmed[Public.latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator)

    with open(Public.enc_result_path, 'wb') as f:
        pickle.dump(func.serialize(), f)


def BFVEvalFunc2(enc_confirmed, enc_deaths, FIPS_lookup):
    last_week_date = datetime.datetime.strftime(
        datetime.datetime.now(timezone('US/Eastern')) - datetime.timedelta(days=7), '%-m/%-d/%-y')
    FIPSindicator = Public.getFIPSInd(FIPS_lookup, State='New York')
    func = (enc_confirmed[Public.latest_record_date] - enc_confirmed[last_week_date]).dot(FIPSindicator)

    with open(Public.enc_result_path, 'wb') as f:
        pickle.dump(func.serialize(), f)


FIPS_lookup = Alice.dataProcess('CKKS')
enc_confirmed, enc_deaths = Carol.fetchFHEData('BFV')
result = []

# statistical query
BFVEvalFunc1(enc_confirmed, enc_deaths, FIPS_lookup)
result.append(Alice.decrypt('BFV'))
BFVEvalFunc2(enc_confirmed, enc_deaths, FIPS_lookup)
result.append(Alice.decrypt('BFV'))
print('Average confirmed cases in California and NYS is', round(np.mean(result)))

# knowledge 1 OR/AND knowledge 2
BFVEvalFunc1(enc_confirmed, enc_deaths, FIPS_lookup)
result.append(Alice.decrypt('BFV'))
BFVEvalFunc2(enc_confirmed, enc_deaths, FIPS_lookup)
result.append(Alice.decrypt('BFV'))
print('If confirmed number in either California and NYS exceeds 50k from last week?:', all(i > 50000 for i in result))
