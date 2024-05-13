if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pkg_resources

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

from default_repo.utils.function import query_fileDB

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    execution_date = datetime.strptime(kwargs.get('custom_date'),'%Y-%m-%d') if kwargs.get('custom_date') else kwargs.get('execution_date') # 1997-10-01
    target_date = execution_date - relativedelta(days=1)
    yearMonth_target = datetime.strftime(target_date, '%Y-%m')
    # yearMonth_target = '1996-09'
    yearMonth_list = [
        datetime.strftime(target_date - relativedelta(months=2), '%Y-%m') # '1996-07'
        , datetime.strftime(target_date - relativedelta(months=1), '%Y-%m') # '1996-08'
        ,  datetime.strftime(target_date, '%Y-%m') # '1996-09'
    ]

    filename = "{}{}-{}".format(
        datetime.strftime(target_date, '%Y')
        , datetime.strftime(target_date - relativedelta(months=2), '%b')
        , datetime.strftime(target_date, '%b')
    ) + '.xlsx'
    pathfile = '{}'.format(filename)

    s2_sql = "SELECT * FROM ProductSalesAmountByMonth WHERE yearMonth = '{}'"
    with pd.ExcelWriter(pathfile) as writer:
        for str_ym in yearMonth_list:
            sheet_name = datetime.strftime(datetime.strptime(str_ym,'%Y-%m'),'%b')
            sheet_data = pd.DataFrame(**query_fileDB(s2_sql.format(str_ym)))
            sheet_data.to_excel(writer, sheet_name = sheet_name, index = False)
    
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        pkg_resources.resource_filename(__name__, os.environ['GG_KEY'])
        , scopes=['https://www.googleapis.com/auth/drive'])

    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile(
        {'parents': [{"id": os.environ['GG_FOLDER_ID']}], 'title': filename}
    )
    file1.SetContentFile(pathfile)
    file1.Upload()

    os.remove(pathfile)
    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
