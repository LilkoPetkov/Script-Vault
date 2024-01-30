# FastAPI script vault

FastAPI script vault, which allows to upload all your scripts at one place and share them with other 
users with just a few clicks. The app is made so an admin would have full control over the script vault and would be able to 
share only the scripts they wish the the respective user. 

# Table of contents
* [Installation](#Installation)
* [Setup](#Setup)
* [Technologies](#Technologies)
* [Contibuting](#Contributing)
* [License](#License)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements located in requirements.txt.

```bash
pip install -r requirements.txt
```

#### Postgre setup

The project requires [PostgreSQL](https://www.postgresql.org/download/) . In the link it can be found available 
for all operating systems. In order to create and manage the database it is also needed to download a sql client for example
[PgAdmin](https://www.pgadmin.org/download/).

## Setup

1. Make sure to update the sample_env with the correct details for Postgre and additional services.
2. The **sample_env** file should be renamed to: **.env**
3. After the environment variables are set, it is needed to run the database migrations.
    - ```alembic init alembic```
    - ```alembic upgrade head```
    - ```alembic revision --autogenerate```
4. Start the APP.
5. Current endpoints:
    - **_/users/me_** - Show user details
    - **_/users/all_** - Show all registered users - Requires admin
    - **_/users/user/{user_id}_** - Return specific user id - Requires admin 
    - **_/users/{user_id}/scripts_** - Returns scripts for specific user - Requires admin
    - **_/users/register_** - Register
    - **_/users/login_** - Login
    - **_/users/update_** - Update current user's details PUT
    - **_/users/update_** - Update current user's details PATCH
    - **_/users/delete/{user_id}_** - Delete user - Requires admin
    - **_/scripts/call/{script_id}_** - Calls script
    - **_/scripts/me_** - Review user's own scripts
    - **_/scripts/all_** - Review all uploaded scripts - Requires admin
    - **_/scripts/script/{script_id}_** - Find specific script - Requires admin
    - **_/scripts/add-script_** - Upload a script from local to server - Requires admin
    - **_/scripts/update-path_** - Changes the scripts paths in the database to the correct one, no matter the uploaded directory - Requires admin
    - **_/scripts/assign-script/{script_id}/{user_id}_** - Assign script to user - Requires admin
    - **_/scripts/delete/{script_id}/{user_id}_** - Removes script from user only, not removing it from the server - Requires admin
    - **_/scripts/delete/{script_id}_** - Removes script from the server, database and all users - Requires admin
    - **_/info_** - Information about the API
    - **_/token_** - Token generation for the swagger docs authentication
    - **_/docs_** - Swagger documentation

## Technologies
 - FastAPI
 - Python 3.9 / 3.11
 - pgAdmin 4 v6.21
 - PostgreSQL 13.10 
    

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
