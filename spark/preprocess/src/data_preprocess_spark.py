import argparse
import requests
from pyspark.sql import SparkSession
import re


def get_secret_creds(path):
    with open(path, 'r') as f:
        cred = f.readline().strip('\'')
    f.close()
    return cred


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_url', type=str, help='URL of the data source', required=True)
    args = parser.parse_args()

    data_url = args.data_url

    ''' Remove possible http scheme for Minio '''
    url = re.compile(r"https?://")

    ''' Download data from data source '''
    filename = data_url
    response = requests.get(data_url, allow_redirects=True, verify=False) #ToDo: disable verify False
    if data_url.find('/'):
        filename = data_url.rsplit('/', 1)[1]

    open(filename, 'wb').write(response.content)

    ''' Read data with Spark SQL '''
    spark = SparkSession.builder.getOrCreate()
    df_data = spark.read.csv(path=filename, sep=",", header=True, inferSchema=True)
    df_data.head()
    df_data.printSchema()

    print("Number of records: " + str(df_data.count()))
