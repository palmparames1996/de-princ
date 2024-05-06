if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from default_repo.utils.function import connection_fileDB, query_fileDB

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    execution_date = datetime.strptime(kwargs.get('custom_date'),'%Y-%m-%d') if kwargs.get('custom_date') else kwargs.get('execution_date')
    # '1997-01-01'
    date_target = datetime.strftime(execution_date, '%Y-%m-%d')
    s3_sql = """SELECT p.SupplierID, o.ShipCountry, ROUND(MAX(JULIANDAY(o.ShippedDate) - JULIANDAY(o.OrderDate)),1) as 'duration(day)',
    '{}' as was_calculated_to, '{}' as last_updated_at
    FROM 'Order Details' as od
    LEFT JOIN 'Orders' as o on od.'OrderID' = o.'OrderID'
    LEFT JOIN Products as p on od.ProductID = p.ProductID
    GROUP BY 1, 2
    """.format(date_target, date_target)

    s3_result = pd.DataFrame(**query_fileDB(s3_sql))

    con_db = connection_fileDB()
    s3_result.to_sql(name='SupplierShipDuration', con=con_db, index=False, if_exists='append')
    con_db.close()

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
