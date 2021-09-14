## How to Use the DS API

Main URL: http://family-promise-dev.us-east-1.elasticbeanstalk.com

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

### `/genders_served` endpoint
Returns an list displaying the total number of recipients of each gender
in the database.

### `/races_served` endpoint
Returns a list displaying the total number of recipients of each race in the
database.

### `/ethnicities_served` endpoint
Returns a list displaying the total number of recipients of each ethnicity in 
the database.

### `/program_enrollment` endpoint
Returns a list displaying the total number of services done that fall under each
program.

### `/services_given` endpoint
Returns a list displaying the total number of each service done.

### `/locations_of_service` endpoint
Returns a list displaying the total number of services given at each type of location
in the database.

[Docs](https://docs.labs.lambdaschool.com/data-science/)

### Running the DS application

- Create the .env file in the folder.
  - Add `DATABASE_URL = postgresql://docker:****@localhost:5400/api-dev` to the .env file.
    - That is only for spinning up the local instance for the DS API
  - Make sure the .env file matches the .env file that is in the non public documentation.
- run:`pipenv install --dev` to download all the dependencies.
- run:`pipenv shell` to start the pipenv environment.
- run:`uvicorn app.main:app --reload` to start running the fast api.

### Running the DS application with Apple M1

- When you `pipenv install --dev` on the M1 you will most likely run into issues where the Pipfile will fail to lock due to issues with psycopg2. Psyocopg2 specifically has issues pip installing on the M1. After figuring out past issues with the M1, this is a work around until there is further bug fixing on compatibility.
- Install Homebrew.
  - [Homebrew](https://brew.sh/)
- Install miniforge for arm64(Apple Silicone M1).
  - [miniforge Github](https://github.com/conda-forge/miniforge).
  - This will not work with Anaconda.
- run: `conda create --name NAME python=3.8`: creates a conda environment.
- run: `conda activate NAME`: activates the conda environment.
  - The conda environment needs to running in order for the application to run.
- run: `conda install -c conda-forge -y psycopg2 numpy pandas`: install necessary dependencies.
- Create the .env file in the folder and continue following the instructions in the section above.

### Updating the Elastic Beanstalk environment

1. Do a normal push to GitHub repo and wait for the changes to be approved and pushed to the main branch.
2. run:`git pull` to make sure code is perfect to deploy to Elastic Beanstalk.
3. run:`git add --all` to get all the changes to the api that has been made.
4. Change the version number in the `main.py` file. Example: `0.37.01`
  - run:`git commit -m 'Depoying version 0.XX.XX to AWS'` to get all the changes add.
  - When you start to deploy the new changes to Elastic Beanstalk it will take latest commit you made.
5. run: `eb init --region us-east-1 family-promise` to create the Elastic Beanstalk files in the application.
   - This step will only be required if you have not deployed to the Elastic Beanstalk environment.
6. run:`eb deploy --region us-east-1 family-promise-dev`.
  - Follow instruction that will given to you.
  - You may have to grab your security credentials from AWS.
7. Do a final push to add the final version number to the GitHub repo.

## Contributors

## **Data Science Team (September, 2021)**

|                                          [Collin Jensen](https://github.com/collinjensen)                                          |                                       [Jeremiah Evangelista](https://github.com/mramputatoes)                                        |                                             [Paul Santora](https://github.com/santorap)                                             |
| :-------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------: |
|       [<img src="https://avatars.githubusercontent.com/u/28957442?v=4" width = "200" />](https://github.com/collinjensen)       |      [<img src="https://avatars.githubusercontent.com/u/81700476?v=4" width = "200" />](https://github.com/mramputatoes)       |            [<img src="https://avatars.githubusercontent.com/u/77029484?v=4" width = "200" />](https://github.com/santorap)             |
|                    [<img src="https://github.com/favicon.ico" width="32"> ](https://github.com/collinjensen)                    |                   [<img src="https://github.com/favicon.ico" width="32"> ](https://github.com/mramputatoes)                    |                          [<img src="https://github.com/favicon.ico" width="32"> ](https://github.com/santorap)                           |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="32"> ](https://www.linkedin.com/in/collin-jensen-b29766146/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="32"> ](https://www.linkedin.com/in/jeremiah-evangelista-6ba928157/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="32"> ](https://www.linkedin.com/in/PaulSantora/) |

|                                      [Sam Ebner](https://github.com/ebnersam)                                      |                                         [Samantha Temple](https://github.com/sntemple12)                                         |
| :-----------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: |
|     [<img src="https://avatars.githubusercontent.com/u/84925046?v=4" width = "200" />](https://github.com/ebnersam)      |      [<img src="https://avatars.githubusercontent.com/u/79993685?v=4" width = "200" />](https://github.com/sntemple12)      |
|                  [<img src="https://github.com/favicon.ico" width="32"> ](https://github.com/ebnersam)                   |                    [<img src="https://github.com/favicon.ico" width="32"> ](https://github.com/sntemple12)                    |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="32"> ](https://www.linkedin.com/in/sam-ebner/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="32"> ](https://www.linkedin.com/in/samantha-temple-487a3620a/) |

<br>
