if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from default_repo.utils.function import connection_fileDB, query_fileDB

import numpy as np
import pandas as pd
import re
import rsa

def getNumberOnly(text):
    return ''.join(re.findall(r'\d+', text))

def encrypting_func(text, publicKey):
    if type(text) == str:
        text = rsa.encrypt(text.encode(),  publicKey)
    return text


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    publicKey, privateKey = rsa.newkeys(1024)

    Customers = pd.DataFrame(**query_fileDB('SELECT * FROM Customers'))
    Customers['Phone'] = list(map(getNumberOnly,Customers['Phone'].fillna(value='')))
    Customers['Fax'] = list(map(getNumberOnly,Customers['Fax'].fillna(value='')))
    Customers = Customers.fillna(value=np.nan).replace('',np.nan,regex=True)
    Customers['Phone'] = list(map(encrypting_func, Customers['Phone'], [publicKey]*len(Customers)))
    Customers['Fax'] = list(map(encrypting_func,Customers['Fax'], [publicKey]*len(Customers)))
    Customers['ContactName'] = list(map(encrypting_func,Customers['ContactName'], [publicKey]*len(Customers)))
    Customers['Address'] = list(map(encrypting_func,Customers['Address'], [publicKey]*len(Customers)))
    Customers['CompanyName'] = list(map(encrypting_func,Customers['CompanyName'], [publicKey]*len(Customers)))
    con_db = connection_fileDB()
    Customers.to_sql(name='Customer', con=con_db, index=False, if_exists='replace')
    con_db.close()

    Suppliers = pd.DataFrame(**query_fileDB('SELECT * FROM Suppliers'))
    Suppliers['Phone'] = list(map(getNumberOnly,Suppliers['Phone'].fillna(value='')))
    Suppliers['Fax'] = list(map(getNumberOnly,Suppliers['Fax'].fillna(value='')))
    Suppliers = Suppliers.fillna(value=np.nan).replace('',np.nan,regex=True)
    Suppliers['CompanyName'] = list(map(encrypting_func,Suppliers['CompanyName'], [publicKey]*len(Customers)))
    Suppliers['ContactName'] = list(map(encrypting_func,Suppliers['ContactName'], [publicKey]*len(Customers)))
    Suppliers['Address'] = list(map(encrypting_func,Suppliers['Address'], [publicKey]*len(Customers)))
    Suppliers['Phone'] = list(map(encrypting_func,Suppliers['Phone'], [publicKey]*len(Customers)))
    Suppliers['Fax'] = list(map(encrypting_func,Suppliers['Fax'], [publicKey]*len(Customers)))
    Suppliers['HomePage'] = list(map(encrypting_func,Suppliers['HomePage'], [publicKey]*len(Customers)))
    con_db = connection_fileDB()
    Suppliers.to_sql(name='Supplier', con=con_db, index=False, if_exists='replace')
    con_db.close()
    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
