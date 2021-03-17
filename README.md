# Airflow Pipeline Project
## Introduction
In this project, we explore the **Apache Airflow** environment to automate, schedule and monitor an end-to-end data engineering pipeline for the Sparkify pseudo start-up. The source data resides in **AWS S3** and needs to be processed in Sparkify's data warehouse in **Amazon Redshift**. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Redshift setup
To kick off the project, we needed to set up an instance of AWS Redshift as our data warehouse. We had already done this previously, so we could leverage the [Redshift Cluster Setup Jupyter Notebook](https://github.com/jfvanreu/AWS-DataWarehouse/blob/main/RedshitClusterSetup.ipynb) to perform this task.

Once we initiated the Redshift data warehouse, we could verify that it was up and running. We received an IP address and could log into it via AWS Console. 

## Launching Airflow
An Airflow server was provided to us for this project. Otherwise, check [Apache Airflow web-site](https://airflow.apache.org/) on how to install the Airflow server.
To start the server, we used the **/opt/airflow/start.sh** command.

## Airflow Connectors
Once the Airflow server is up and running, we need to create connections/hooks to the Redshift cluster which we launched previously. Those connections will be used as part of our operators/scripts.

**IMPORTANT NOTE:** Both Amazon Web Service and Redshift database hooks must be set with the right configuration for the airflow pipeline to succeed.

### Amazon Web Services hook
To connect to Redshift and S3, we need to have some AWS user credentials. Those can be set in the Airflow/Admin/Connections tab by filling in the following fields. Note that Redshift uses a "Postgres" connection type. Also, we need valid AWS credentials for a user that has access to Redshift cluster.

### Redshift database
We also need to define the settings of a redshift "hook". This allows us to connect to our Redshift cluster. When we created the Redshift cluster, we also created a database schema and user who can access this database. This information is key to connect to Redshift via Airflow. See below the info that needs to be provided.

## Creating tables in Redshift using a DAG
Before copying data to a database, we first needed to create the various staging and STAR model FACTS and DIMENSIONS tables. We decided to create a specific DAG to perform this operation. The DAG first deletes each table and then creates new one. This was a good way to get our feet wet with Airflow.

## Main Sparkify pipeline
We designed the main Sparkify pipeline as shown on the workflow diagram below.

The pipeline first connects to AWS S3 to collect songs and logs data. Using this data, it creates the FACT table SONGPLAYS which includes a history of the various songs played by customers. The pipeline also creates Dimension tables for Artists, Songs, Users, and Time. This is the STAR schema that we have used in previous Sparkify projects. The database schema is available below ![database schema](https://github.com/jfvanreu/AWS-DataWarehouse/blob/main/images/DBdesign.jpeg).

For this project, you'll be working with two datasets. Here are the s3 links for each:

Log data: s3://udacity-dend/log_data
Song data: s3://udacity-dend/song_data

The log data is partinioned by time (year, month). We made sure that Airflow only picked up the data that was relevant to its execution time. The script only looked at the data available at that time and didn't load the entire log data set.

The song data set was loaded for each run. This is a bit redundant when we backtrack (work in the past) since we transfer the same data from S3 over and over. However, we can assume that the Airflow pipeline would mostly be run on a daily basis in the future, so this situation wouldn't occur too often.  

As a last step in our pipeline, we perform some basic quality checks to verify that the tables have been populated as expected.

## Results
We ran our pipeline on a provided data set and within an allocated time frame (Nov 2018). The pipeline performed well as shown below.
Because we set a start date in the past, Airflow was smart enough to backtrack to that time and collect the matching data.

## Lessons Learned

## Improvements opportunities
This project provides a good introduction to Airflow but it can be improved in multiple ways:
- Create some sub-dags to collect data from S3 and create dimension tables.
- Further develop the quality check operator
- 
## Conclusion
