from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import create_tables as sql_statements

dag = DAG('create_tables_dag',
          description='Drop and create tables in Redshift with Airflow',
          start_date=datetime.now(),
          schedule_interval=None
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_artists_table = PostgresOperator(
    task_id="create_artists_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_ARTISTS_TABLE_SQL, sql_statements.CREATE_ARTISTS_TABLE_SQL]
)

create_songs_table = PostgresOperator(
    task_id="create_songs_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_SONGS_TABLE_SQL, sql_statements.CREATE_SONGS_TABLE_SQL]
)

create_songplays_table = PostgresOperator(
    task_id="create_songplays_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_SONGPLAYS_TABLE_SQL, sql_statements.CREATE_SONGPLAYS_TABLE_SQL]
)

create_staging_events_table = PostgresOperator(
    task_id="create_staging_events_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_STAGING_EVENTS_TABLE_SQL, sql_statements.CREATE_STAGING_EVENTS_TABLE_SQL]
)

create_staging_songs_table = PostgresOperator(
    task_id="create_staging_songs_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_STAGING_SONGS_TABLE_SQL, sql_statements.CREATE_STAGING_SONGS_TABLE_SQL]
)

create_users_table = PostgresOperator(
    task_id="create_users_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_USERS_TABLE_SQL, sql_statements.CREATE_USERS_TABLE_SQL]
)

create_time_table = PostgresOperator(
    task_id="create_time_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=[sql_statements.DROP_TIME_TABLE_SQL, sql_statements.CREATE_TIME_TABLE_SQL]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_artists_table
start_operator >> create_songs_table
start_operator >> create_users_table
start_operator >> create_time_table
start_operator >> create_songplays_table
start_operator >> create_staging_events_table
start_operator >> create_staging_songs_table
create_artists_table >> end_operator
create_songs_table >> end_operator
create_users_table >> end_operator
create_time_table >> end_operator
create_songplays_table >> end_operator
create_staging_events_table >> end_operator
create_staging_songs_table >> end_operator


