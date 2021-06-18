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


### `/veteran_counts` enpoint
A JSON object containing:

- recipient_id
- recipient_veteran_status

from `recipients` table.





[Docs](https://docs.labs.lambdaschool.com/data-science/)
