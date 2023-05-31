from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
from spotify_auth import get_spotify_auth_url

default_args = {
    'start_date': datetime(2023, 5, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'spotify_auth_dag',
    default_args=default_args,
    description='Spotify Authorization DAG',
    schedule_interval=None
)

load_dotenv()

def authorize_spotify():
    auth_url, state = get_spotify_auth_url()
    # Store auth_url and state in a database or any other mechanism

    # to be used later in the callback
    print(f'Authorization URL: {auth_url}')
    print(f'State: {state}')

authorize_task = PythonOperator(
    task_id='authorize_spotify',
    python_callable=authorize_spotify,
    dag=dag
)

authorize_task
