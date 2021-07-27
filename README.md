## How to Use the DS API

Main URL: http://family-promises-db.eba-saefv7mf.us-east-1.elasticbeanstalk.com

### `/vizmap` endpoint

Perform SQL query of database according to filters implemented by user.
Only pick out the following columns, and include those in a single JSON object that will be sent to DS API:

- `service_type_name` from `service_types` table.

Plus:

- address
- address_line2
- city
- state
- zip
- country

from `locations` table.

*zip codes are pulled from github repo link and added to a dataframe based on pulled zip

### `/veteran_counts` endpoint
A JSON object containing:

- recipient_id
- recipient_veteran_status

from `recipients` table.


### `/age_metric` endpoint
A JSON object containing:

- recipient_id
- recipient_date_of_birth

from `recipients` table.

### `/eligibility` endpoint
Accepts a string containing a household_id from the
households table.

Returns a JSON object containing:

- resident_assistance_eligibility: bool
- reduced_bus_fare_eligiblity: bool

### `/total_served` endpoint
Returns an integer representing the total number of recipients recorded in the
database.

### `/families_served` endpoint
Returns an integer representing the total number of families recorded in the
database.

### `/children_served` endpoint
Returns an integer representing the total number of children recorded in the
database.


[Docs](https://docs.labs.lambdaschool.com/data-science/)
