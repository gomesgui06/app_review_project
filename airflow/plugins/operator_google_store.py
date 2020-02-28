import logging
import sys


from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin

#from airflow.crawler_google_store import CrawlerApp


logging.basicConfig (stream = sys.stdout,
                     level = logging.INFO,
                     format = '%(asctime)s;%(levelname)s;%(message)s',
                     datefmt = '%m/%d/%Y %I:%M:%S %p')


class GoogleStoreToDataLakeOperator(BaseOperator):

    @apply_defaults
    def __init__(self, app_id, language, output, *args, **kwargs):
        super(GoogleStoreToDataLakeOperator, self).__init__(*args, **kwargs)
        self.app_id = app_id,
        self.language = language,
        self.output = output

    def execute(self, context):
        logging.info('Crawler start')

'''

        CrawlerApp(app_id=self.app_id,
                   language=self.language,
                   output=self.output).run_reviews()
'''


class GoogleStoreToDataLakePlugin(AirflowPlugin):
    name = 'GoogleStorePlugin'
    operator = [GoogleStoreToDataLakeOperator]
