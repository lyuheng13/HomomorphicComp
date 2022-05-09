import Public
import Alice
import Carol


# 1. CKKS scheme
# Alice: data preprocess
Alice.CKKSSetup()
FIPS_lookup = Alice.dataProcess('CKKS')

# Carol: work on query function
enc_confirmed, enc_deaths = Carol.fetchFHEData('CKKS')
enc_result = Carol.CKKSEvalFunc(enc_confirmed, enc_deaths, FIPS_lookup)

# Alice: decrypt encrypted result
Alice.decrypt('CKKS')


# 2. BFV scheme
# Alice: data preprocess
Alice.BFVSetup()
FIPS_lookup = Alice.dataProcess('BFV')

# Carol: work on query function
enc_confirmed, enc_deaths = Carol.fetchFHEData('BFV')
enc_result = Carol.BFVEvalFunc(enc_confirmed, enc_deaths, FIPS_lookup)

# Alice: decrypt encrypted result
Alice.decrypt('BFV')
