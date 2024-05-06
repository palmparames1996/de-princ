if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import boto3
import os


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    s3 = boto3.client("s3")

    s3.download_file(
        Bucket = os.environ['BUCKET_NAME'] 
        , Key="init/client_secrets.json"
        , Filename = os.environ['GG_KEY']
    )

    s3.download_file(
        Bucket = os.environ['BUCKET_NAME']
        , Key="init/medcury-de.db"
        , Filename = os.environ['DB_FILE']
    )

    return True


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
