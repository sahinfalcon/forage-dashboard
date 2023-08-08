# Forage Dashboard

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


