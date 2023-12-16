<h1 align="center" id="title">Smogboard v1</h1>

<p align="center"><img src="https://img.shields.io/badge/data%20engineering-8A2BE2" alt="shields"> <img src="https://img.shields.io/badge/google cloud platform-00A36C" alt="shields"> <img src="https://img.shields.io/badge/python-48BBDB" alt="shields"></p>

<p id="description" align="center">An end-to-end data engineering project using data sources from Smogon Stats and PokeAPI.</p>

<h2>🧑‍🔧 Data Pipeline</h2>
 
*   Mage was in charge of my ETL processes and scheduling/orchestration because people were hyping it as the next Airflow.
*   BigQuery handled my Data Warehousing needs and it was effortless connecting it to Looker Studio as a live source.
*   Yes it's nothing fancy, but hey - it works.

![pipeline](https://i.imgur.com/jFOsdjZ.png)

<h2>🌟 Data Model</h2>

*   I used Kimball's approach for data warehousing (transaction-based) and created the star schema below.
*   Again, nothing fancy because I didn't want to overcomplicate this project.

![model](https://i.imgur.com/oHDpZBX.png)

<h2>🚀 Demo</h2>

*   The final result (yes it needs some work):

![dashboard](https://i.imgur.com/7LWueEP.png)

[Click here to interact with it!](https://lookerstudio.google.com/reporting/7e7e3a41-7147-485c-be44-e1428af05d7a)

<h2>💻 Built With</h2>

Technologies used in the project:

*   Python
*   Mage
*   Google Cloud Platform
*   BigQuery
*   Looker Studio

<h2>👀 What's Next</h2>

*   Including statistics for other generations and battle formats
*   Improve on the dashboard's design and naming consistency of fields
*   Enhance dashboard visuals with sprites and type-based coloring

<h2>🛡️ License</h2>

This project is licensed under the MIT License.
