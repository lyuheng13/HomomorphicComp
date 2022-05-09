# Computation Ove Encrypted Data

This project is a remote calculation over homomorphic encrypted data based on JHU CSSE COVID-19 Data.

## Feature
The program allows to retrieve and calculate the confirmed cases of Coivd-19 of a given state within a given period of time. All the data during the caculation will be encrypted with FHE. Therefore, no senstitive data will be exposed.

The script Alice will imitage the behavior of data owner that requests a remote homomorphic calculation.

The script Carol will imitage the behavior of a server receiving encrypted data and produce homomorphic encrypted output back to Alice without knowing the actual content.

## Installation

```bash
$ pip install tenseal
```

## Team Member
Ruichen Yang \
Yuheng Zhong
