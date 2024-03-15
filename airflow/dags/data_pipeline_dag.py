from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('advertiseX_data_pipeline',
          default_args=default_args,
          description='DAG for AdvertiseX data processing pipeline',
          schedule_interval=timedelta(days=1),
          catchup=False)

def run_kafka_producer():
    from producers.kafka_producer import run_kafka_producer
    run_kafka_producer()

produce_task = PythonOperator(
    task_id='run_kafka_producer',
    python_callable=run_kafka_producer,
    dag=dag,
)

# Path to your PySpark script
spark_script_path = os.path.join(os.environ.get('AIRFLOW_HOME', ''), 'spark_jobs', 'pyspark_job.py')

# Bash command to submit the Spark job
spark_submit_cmd = f"""
export AWS_ACCESS_KEY_ID={os.environ.get('AWS_ACCESS_KEY_ID')}
export AWS_SECRET_ACCESS_KEY={os.environ.get('AWS_SECRET_ACCESS_KEY')}
export S3_BUCKET_NAME={os.environ.get('S3_BUCKET_NAME')}
spark-submit --master local[2] {spark_script_path}
"""

spark_task = BashOperator(
    task_id='run_spark_job',
    bash_command=spark_submit_cmd,
    dag=dag,
)

produce_task >> spark_task
