# Data Engineering Final Project

Welcome to the Forage Dashboard repository! This project is a part of the Data Engineering Makers specialist track and aims to create a real-time dashboard for Global Education Insights (GEI) to visualize and interpret data from the PISA 2018 dataset.

## About Global Education Insights (GEI)

Global Education Insights (GEI) is a non-profit organization dedicated to improving education systems worldwide. They work with governments, educational institutions, and stakeholders to provide data-driven insights and recommendations for educational policy and practice.

## Project Overview

The goal of this project is to leverage data engineering skills to analyze the PISA 2018 dataset and develop a functioning dashboard that GEI can use to easily visualize and interpret the data. The project is carried out in a distributed environment in the Cloud to allow for efficient data processing and collaboration.

## Project Objectives

The project has three levels of challenge:

- **Level 1:** Develop Forage charts displaying correct summary data that is no more than an hour old.
- **Level 2:** Same as Level 1, but the data should be no more than a minute old.
- **Level 3:** Same as Level 2, but the data should be up-to-the-second.

## Solution Overview

The Forage Dashboard solution is a sophisticated real-time data visualization tool built with a Flask web application written in Python. Hosted on a render.com web service, this application connects seamlessly to an AWS RDS (Relational Database Service) for PostgreSQL, enabling access to data from the PISA 2018 dataset. The solution's architecture encompasses multiple layers to ensure accurate, up-to-date, and comprehensive insights.

### Flask Web Application

The cornerstone of the solution is the Flask web application, which orchestrates data retrieval, processing, and presentation. This app exposes a range of API endpoints to allow users to interact with and query the dataset in real time. Each endpoint corresponds to a unique visualization or data summary, facilitating intuitive exploration.

### AWS RDS and Airflow Integration

The data ecosystem that powers the Forage Dashboard is orchestrated through an AWS Relational Database (RDS) for PostgreSQL. This RDS is a central repository updated by a set of 20 Apache Airflow DAGs. These DAGs continuously collect updated data from 20 distinct AWS RDS sources, ensuring that the central RDS is always populated with the latest information.

### SQL Queries for Data Insights

The Flask app employs carefully crafted SQL queries to extract meaningful insights from the AWS RDS. These queries enable the dashboard to offer key features, including:

- **Submission Count:** A simple query counts the total number of submissions, providing a comprehensive overview.

- **Average Learning Hours per Week:** Calculating the average learning hours per week involves a query that aggregates and processes relevant data.

- **Economic, Social, and Cultural Scores (ESCs):** The average ESC scores are derived through a query that aggregates ESC-related data.

- **Early Education and Sense of Belonging:** Similar to the ESCs, average scores for early education and sense of belonging are calculated using queries that aggregate pertinent data.

- **Submissions Over Time:** The submissions-over-time feature utilizes queries that extract the number of submissions at various hours throughout the day.

### Render.com and Seamless Deployment

Render.com serves as the hosting platform for the Flask application. The web service ensures the dashboard is accessible, responsive, and scalable. This seamless deployment and scaling enable GEI to access the dashboard from any device, fostering a user-friendly experience.

### Empowering Data-Driven Decisions

Through the integration of Flask, PostgreSQL, AWS RDS, and Airflow, the Forage Dashboard provides GEI with a powerful tool to make informed decisions about education systems worldwide. By visualizing real-time data, GEI can identify trends, patterns, and areas for improvement, ultimately contributing to enhanced educational policies and practices.


## Contents

- [Setup Instructions](#setup-instructions)
- [File Structure](#file-structure)
- [License](#license)

## Setup Instructions

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/Forage-Dashboard.git
   cd Forage-Dashboard

2. Install dependencies

     ```bash
     pip install -r requirements.txt

3. Setup your configuration
    Create a config.py file

4. Run the dashboard

    ```bash
    python dashboard.py

## File Structure

The project directory has the following structure:

- `.gitignore`: Specifies files and directories ignored by Git.
- `Procfile`: Used by Heroku to specify commands for deploying.
- `config.py`: Configuration file for storing environment variables.
- `dashboard.py`: Main script for generating endpoint APIs for the dashboard.
- `requirements.txt`: List of project dependencies.

## License

This project is licensed under the MIT License.

For more information about the Data Engineering Makers specialist track, visit the [Makers Academy Brochure](https://drive.google.com/file/d/1ld6IdZLX3p0bslw2bnD3uTy6WsBT9JHz/view).


