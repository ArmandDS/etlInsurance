============================================
ETL on the Agency Performance Model
============================================



ETL process to load and summarize the data on the Agency Performance Model dataset on Kaggle: https://www.kaggle.com/moneystore/agencyperformance
The API impleted is secure througt jwt and token authorization.
I created a web Dasboard with some visualizations.


Developments
============
I designed an star shecheme for the file like you can see below

-  Revenues: The fatcs
-  Product: Dimension
-  Agencies: Dimension
-  Cluster: Dimension

I implemented the following methods for reporting:

1.  Profitability: To extract a profitability report by product for the agency by and year.
2.  Cash Flow: To extract a cashflow report by product by agencies and years
3.  Revenues: To extract a revenue report by product by agencies and years
4.  Products: to extract all products
5.  Agencies: to get all agencies


**Categorization**

We implemented the K-Mean algorithm in order to Clustering the agencies based in similarities and to find groups(clusters) in the given data.


Project File Structure
========================
The files on this project::

	+flaskAppETL/
	| +--- application.py:      the server file
	| +--- config.py :          the configuration file, here is the database URI, the jwt inicialization
	| +--- etl.log :            log of the server
	| +--- models.py:           the sqlalchemy database model for users
	| +--- README.rst
	| +--- requirements.txt
	| +--- resources.py:        the API file where we call the API endpoints
	| +--- views.py:            the route file, where the views are created 
	  |
	  +api/
	  | +--- report.py:         the end point file where the report are created
	  |
	  +data/
	  | +--- etl.py:            the ETL file, where we cleaning and loading the data to database 
	  | +--- finalapi.csv
	  |
	  +static/
	    |
	    +css/
	    | +--- custome.css:      our css stylesheet
	    | +--- sb-admin.css
	    | +--- sb-admin.min.css
	    |
	    +js/
	    | +--- customer.js:      our main Javascript file, handles the load of charts, the tables and the ajax request
	  |
	  +templates/
	  | +--- dashboard.html:     the html of the main dashboard
	  | +--- signin.html:        the index file






Instructions
============

The package can be installed with pip using the following command:

.. code-block:: bash

    $ git clone https://github.com/armandDs/test_britcore.git

Next, install the dependencies:

.. code-block:: bash

    $ pip install -r requirements.txt

To run the server on localhost:

.. code-block:: bash

    $ python application.py



REST API
========

I implemented A REST API based on the above ETL process working with mysql + elasticbeanstalk from aws, with secure token API

1. Currently there is only 1 user:**guest** with password: **guest**
2. I secured the API wth jwt in flask
3. I implemeted a Dashboard single page web  with Javascrtip, Jquey, datatable, flask and chart.js for the visualization

you can use the API using curl or postman:
please login with the credentials and get the token (this token will expires in 1 hour)

.. code-block:: bash

	$curl -X POST -F username=guest -F password=guest http://localhost:5000/login

Save the authorizaton token and send it with every api request, for example to request all products **/allproducts** dimension:

.. code-block:: bash

	curl -X GET http://flaskapp1-dev22.us-west-2.elasticbeanstalk.com/allproducts  -H "authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTY5OTI2MDUsIm5iZiI6MTU1Njk5MjYwNSwianRpIjoiNzMyZWRkM2QtN2YxMi00MzMzLTkyNWMtYzEyMDAxMDIzYzYxIiwiZXhwIjoxNTU2OTk2MjA1LCJpZGVudGl0eSI6ImFybWFuZDIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.bCUipAp6h6BzX-gohHLmBq39sXhEUYhy6AZXlW94lT4" 

this return the list of products in json format.



to request a profitabilty report for agency 16 for all years  **/profitability/agency/16** :

.. code-block:: bash

	curl -X GET http://flaskapp1-dev22.us-west-2.elasticbeanstalk.com/profitability/agency/16  -H "authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTY5OTI2MDUsIm5iZiI6MTU1Njk5MjYwNSwianRpIjoiNzMyZWRkM2QtN2YxMi00MzMzLTkyNWMtYzEyMDAxMDIzYzYxIiwiZXhwIjoxNTU2OTk2MjA1LCJpZGVudGl0eSI6ImFybWFuZDIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.bCUipAp6h6BzX-gohHLmBq39sXhEUYhy6AZXlW94lT4" 

this return the list of products in json format.



The Completed end points implemented are:
------------------------------------------

- '/cashreport': get all agencies cash flow report data 
- '/cashreport/agency/agency_id': get only cash flow report data from agency id equal to agency_number (json format)
- '/profitability': get all agencies profitabilities report data (json format)
- '/profitability/agency/agency_id': get all only profitabilities report data of a particular agency (json format)
- '/profitability/agency/agency_id/year/year_number':  get all only profitabilities report data of a particular agency and year (json format), i.e the data that meet the criteria.
- '/alldata': Downdload CSV 
- '/allagencies': get all agencies dimension (json format) 
- '/allproducts': get all products dimension (json format) 
- '/revenues':  get all agencies revenues report data (json format)
- '/revenues/agency/agency_id':  get all only revenues report data of a particular agency (json format)
- '/revenues/agency/agency_id/year/year_number': get all only revenues report data of a particular agency and year (json format), i.e the data that meet the criteria.
- '/clustering': get the cluster classification of the agencies (json format)




THE WEB DASHBOARD
===============

As I said you can explore the dashboard throught the site:
http://flaskapp1-dev22.us-west-2.elasticbeanstalk.com/

login the credentials above, and see the single page I implemented with Javascript, Jquery, Datatable and Chart.js, and styles with boostrap.

note: the database is created/populated at the very first request after you started the sever 



Some of the views of the dashboard:
------------------------------------------


The Profitability report for agency 102 and year 2010:


.. image:: /static/images/1.PNG
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text

The cash flow for agency 45 and last 5 years:


.. image:: /static/images/2.PNG
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text


.. image:: /static/images/3.PNG
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text


The revenue report for agency 1010 and year 2014:


.. image:: /static/images/4.PNG
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text


The clustering of agencies:


.. image:: /static/images/5.PNG
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text



Command Line Interface
======================

first go to folder data:

.. code-block:: bash

    $ cd data

To load the finalapi.csv dataset into the database run the following command:

.. code-block:: bash

    $ python etl.py

the to run the reports go to API folder data:

.. code-block:: bash

    $ cd ../api



To display a revenue report by product for the agency with the id 16 for the past 5 years run the following command (to export to a csv instead, add --dest or -d csv):

.. code-block:: bash

    $ python report.py revenue 3 --dest print


To export a profitability report by product for the agency with the id 3 for the year 2011 run the following command (to display in stdout instead of exporting to a csv, remove --dest csv):

.. code-block:: bash

    $ python etl.py profitability 3 2011 --dest csv

To display a cashflow report by product for the agency with the id 3 for the past 5 years run the following command (to export to a csv instead, add --dest csv):

.. code-block:: bash

    $ python report.py cash_report 3 --dest print


To export a clster report run the following command (to export to a csv instead, add --dest csv):

.. code-block:: bash

    $ python report.py cluster --dest csv
