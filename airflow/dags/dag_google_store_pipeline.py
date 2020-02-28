from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta


from airflow.operators import GoogleStoreToDataLakeOperator


default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('test',
          default_args = default_args,
          schedule_interval = timedelta(days=1))

start_dag = DummyOperator(
    task_id = 'start',
    default_args = default_args,
    dag = dag)

end_dag = DummyOperator(
    task_id = 'end',
    default_args = default_args,
    dag = dag)


google_store_dag = GoogleStoreToDataLakeOperator(
    task_id = 'google_store_dag',
    default_args = default_args,
    dag = dag,
    # app_id = 'TESTE',
    # language = 'pt',
    # output = 'TESTE'
    app_id = 'br.com.sky.selfcare',
    language = 'en',
    output = '')


start_dag >> google_store_dag >> end_dag
