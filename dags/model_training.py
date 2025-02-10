"""
MLOps Pipeline for Continuous Model Training
"""
from airflow.operators.python import PythonOperator
from services.model_retrainer import ModelRetrainer

def create_training_dag():
    dag = DAG(
        'model_retraining',
        schedule_interval='@weekly',
        default_args={'start_date': datetime(2023, 1, 1)}
    )
    
    with dag:
        fetch_task = PythonOperator(
            task_id='fetch_new_data',
            python_callable=fetch_from_data_warehouse
        )
        
        validate_task = PythonOperator(
            task_id='validate_data',
            python_callable=run_data_validation
        )
        
        train_task = PythonOperator(
            task_id='train_new_model',
            python_callable=ModelRetrainer().periodic_retraining
        )
        
        deploy_task = PythonOperator(
            task_id='deploy_model',
            python_callable=update_production_model
        )
        
        fetch_task >> validate_task >> train_task >> deploy_task
    return dag 