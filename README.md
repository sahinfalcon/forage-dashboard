# Data Engineering Final Project

Welcome to the Forage Dashboard repository! This project is a part of the Data Engineering Makers specialist track and aims to create a real-time dashboard for Global Education Insights (GEI) to visualise and interpret data from the PISA 2018 dataset.

## About Global Education Insights (GEI)

Global Education Insights (GEI) is a non-profit organisation dedicated to improving education systems worldwide. They work with governments, educational institutions, and stakeholders to provide data-driven insights and recommendations for educational policy and practice.

## Project Overview

The goal of this project is to leverage data engineering skills to analyse the PISA 2018 dataset and develop a functioning dashboard that GEI can use to easily visualise and interpret the data. The project is carried out in a distributed environment in the Cloud to allow for efficient data processing and collaboration.

## Project Objectives

The project has three levels of challenge:

- **Level 1:** Develop Forage charts displaying correct summary data that is no more than an hour old.
- **Level 2:** Same as Level 1, but the data should be no more than a minute old.
- **Level 3:** Same as Level 2, but the data should be up-to-the-second.

## Solution Overview

The Forage Dashboard solution is not only feature-rich but also deeply automated and persistent, making it an indispensable tool for Global Education Insights (GEI) to derive data-driven insights in real-time. Let's delve into the details of how this solution remains current and always accessible:

### Stack

#### Backend:
- Python
- Flask: Web framework to build RESTful APIs for data retrieval and serve the frontend.
- Psycopg2: Connects and interacts with the PostgreSQL database.

#### Database:
- Amazon RDS: Cloud-based relational database to store and manage the PISA 2018 dataset.
- PostgreSQL: Database management system used within the Amazon RDS.

#### Data Ingestion and Processing:
- Apache Airflow: Orchestrates the data ingestion process. Airflow DAGs periodically collect data from 20 different source Amazon RDS databases and populate the main analytical RDS.

#### Deployment and Hosting:
- Render: Hosts the Flask application and provides a web server environment.
- Amazon EC2 with tmux: Utilised to run Airflow DAGs persistently.

#### Version Control and Collaboration:
- Git/GitHub: Used for version control, collaborative working, and tracking changes.

### Automated Data Collection and Integration

The foundation of this solution is built upon 20 Apache Airflow DAGs that execute continuously and autonomously. These DAGs orchestrate the collection and integration of data from 20 distinct AWS RDS sources. This process ensures that the central AWS RDS, which the Forage Dashboard relies upon, is continuously updated with the latest information every 30 seconds. By pooling data from these distributed sources, the dashboard guarantees a comprehensive and up-to-date perspective.

### Real-Time Data Visualization

The web application, programmed in Python using Flask and hosted on a render.com web service, takes center stage in delivering real-time insights. As users interact with the dashboard, they're effectively accessing live data from the central AWS RDS. The automated DAGs ensure that the dataset feeding into the dashboard is always reflective of the latest developments, fostering accurate, real-time analysis and decision-making.

### Apache Airflow DAGs: Automation Backbone

The automated data collection and integration process is executed through the use of Apache Airflow DAGs. These DAGs facilitate the seamless extraction, transformation, and loading (ETL) of data from the distributed AWS RDS sources into the central repository. The DAGs ensure the solution's persistence by continuously refreshing the dataset, providing the dashboard with an ever-evolving pool of data.

### Render.com: Continuous Deployment

The Forage Dashboard remains accessible and available. By hosting the Flask application on render.com, the solution achieves continuous deployment, ensuring that the dashboard is always ready to be accessed by GEI. This continuous availability is crucial for maintaining a persistent connection to real-time data insights.

### Empowering Data-Driven Decisions

The deeply automated and persistent nature of the Forage Dashboard empowers GEI to make data-driven decisions without interruption. The Airflow DAGs ensure that the dataset is perpetually refreshed, enabling the visualisation of real-time trends and patterns. Render.com guarantees that the dashboard is always accessible, whether on a desktop or mobile device, enhancing the user experience and fostering effective decision-making.

By combining Apache Airflow's automation capabilities with render.com's continuous deployment, the Forage Dashboard remains an innovative solution that bridges data science and accessibility for informed education policy and practice improvements.


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