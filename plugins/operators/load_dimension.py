from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 append_data=False,
                 sql="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.table=table
        self.sql=sql
        self.append_data=append_data

    def execute(self, context):
        self.log.info('LoadDimensionOperator starts here')
        self.log.info('Connect to Redshift instance')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if not self.append_data:
            self.log.info('Deleting existing records to start fresh like a daisy....')
            sql_statement = "DELETE FROM {}".format(self.table)
            redshift.run(sql_statement)
        #insert (or append) records to the table
        formatted_sql = ("""INSERT INTO {} {}""".format(self.table, self.sql))
        self.log.info("Running this SQL command: {}".format(formatted_sql))
        try:
            redshift.run(formatted_sql)
        except Exception as e:
            self.log.info("Oops! There is a problem with this SQL query: {}".format(e))
        
