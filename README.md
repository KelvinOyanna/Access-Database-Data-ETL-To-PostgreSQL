# Project Description:
This repository contains the code, data and resource used to implement a data ingestion pipeline and analyzing the data to draw-out some insight. The project is part of the requirement for Kippa's data analyst interview process.
On execution, the program downloads the required access database file from: https://msi.nga.mil/Publications/WPI, load the data from the file into a Postgresql database instance on Google Cloud Platform and create tables based on the questions asked.

### Pre-requisite:
In order to run this code, you first need to create an ODBC Data Source Name (DSN) that points to the downloaded Microsoft Access database file in the folder 'data'. Details on how to creat a DSN can be found [on this link](https://www.microfocus.com/documentation/silk-test/210/en/silktestworkbench-help-en/SILKTEST-413CCBCD-CREATINGDATASOURCEACCESSDATABASE-TSK.html). This establish connection to the database file so we can read data from it.

### Setting-up environment:
To setup your environment to run the program, create and activate a virtual environment by running
the following codes on your command-line
 - python3 -m venv name-of-virtual-environment (Create virtual environment)
 - source ./name-of-virtual-environment/bin/activate (Activate environment.)
 - pip -r install requirements.txt (Install libraries/dependencies)
 
Create an environment variable file (.env) to store all database credentials/secrets. Your .env file should take the format below:
- DB_USER_NAME=your_postgreql_database_username
- DB_PASSWORD=your_postgresql_database_password
- DB_NAME=your_postgresql_database_name
- PORT=5432
- HOST=your_postgresql_database_instance_host/IP

### Running the program:
To execute the code from the command line, run below code:
- python3 main.py 

This downloads the required access database file, load data from the file into a postgresql database on Google Cloud and create tables based on the questions asked.
NB: Run the above codes from a shell session in the project directory.

### Output:
A screen-shot of the SQL output of the created tables can be found in directory 'SQL_Output_Screenshots'
