if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from default_repo.utils.function import connection_fileDB, query_fileDB

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    execution_date = datetime.strptime(kwargs.get('custom_date'),'%Y-%m-%d') if kwargs.get('custom_date') else kwargs.get('execution_date') # 1997-01-01
    target_date = execution_date - relativedelta(days=1)
    yearMonth_target = datetime.strftime(target_date, '%Y-%m')
    yearMonth_previous = datetime.strftime(target_date - relativedelta(months=1), '%Y-%m')

    s1_sql = f"""WITH transaction_data AS (
    SELECT o.OrderDate as date, od.'OrderID', od.ProductID, od.UnitPrice * od.Quantity as salesAmount
    FROM 'Order Details' as od
    LEFT JOIN 'Orders' as o on od.'OrderID' = o.'OrderID'
    WHERE STRFTIME('%Y-%m', date) = '{yearMonth_target}'
    ), 

    transaction_by_yearMonth AS (
    SELECT STRFTIME('%Y-%m', date) as yearMonth, ProductID, SUM(salesAmount) as salesAmount
    FROM transaction_data
    GROUP BY 1, 2
    ),

    transaction_by_yearMonth_previous as (
    SELECT ProductID, salesAmount 
    FROM ProductSalesAmountByMonth
    WHERE yearMonth = '{yearMonth_previous}'
    )

    SELECT tby.yearMonth, tby.ProductID, p.ProductName, tby.salesAmount, ((tby.salesAmount/tbyp.salesAmount)-1)*100 as percentage_change
    FROM transaction_by_yearMonth as tby
    LEFT JOIN Products as p on tby.ProductID = p.ProductID
    LEFT JOIN transaction_by_yearMonth_previous as tbyp on tby.ProductID = tbyp.ProductID
    """

    s1_result = pd.DataFrame(**query_fileDB(s1_sql))

    con_db = connection_fileDB()
    s1_result.to_sql(name='ProductSalesAmountByMonth', con=con_db, index=False, if_exists='append')
    con_db.close()
    
    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
