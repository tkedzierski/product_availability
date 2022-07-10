# product_availability
Monitoring prices and availability of products in a selected category in stores based on the prestashop engine. 

Script checks the selected category every set time and reports changes to the e-mail when such occur.

monitored changes:
- price
- availability
- new product in category
- removed product from category

# preparation for launch:
prepare an account at cloud.mongodb.com (free plan) by adding a new cluster, and then configuring the cluster connection to the new app

prepare gmail for sending reports - create a new email or use an existing one

    with the current security policy, two-factor authentication must be enabled on your account
    create a password for the external application in the account settings

## variables in "settings.py" file:
- "url" - website address of the store leading directly to the category
- "MongoClusterURL" - full connection path to the cluster
- "Mongo_DB_pass" - password for the username "user"
- "MongoDB_DB_name" - database name
- "MongoDB_coll_products" - products collection name
- "MongoDB_coll_status" - status collection name
- "MongoDB_coll_archives" - archive status collection name
- "MongoDB_coll_report" - report collection name
- "EmailLogin" - login to gmail account for sending the report
- "EmailPassword" - app password to gmail account for sending the report
- "EmailReportRecipient" - email address of the report recipient

# First use:
- run "installation.py" file to prepare the data from shop
- run "main.py"

      as default, the website is checked every 60 minutes, then if there is a change in monitored values, a report will be send
