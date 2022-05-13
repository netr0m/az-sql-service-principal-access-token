# Microsoft SQL Server -> ODBC connection using service principal access tokens

## Requirements
### Packages
- docker

### The existence of the service principal user in the database
1. Locate the name of your service principal
2. Execute the following statements in the database for which you wish to grant access:
    - This can also be done via the "Query editor" in the Azure Portal for the database in question
    ```sql
    CREATE USER "<SERVICE_PRINCIPAL_NAME>" FROM EXTERNAL PROVIDER;
    EXEC sp_addrolemember '<role_name>', '<SERVICE_PRINCIPAL_NAME>';
    ```
    - To list existing roles, execute the following statement:
    ```sql
    sp_helprole;
    ```
**Known working example:**
```sql
CREATE USER "<SERVICE_PRINCIPAL_NAME>" FROM EXTERNAL PROVIDER;
EXEC sp_addrolemember 'db_datareader', '<SERVICE_PRINCIPAL_NAME>';
```

### Environment variables
```sh
# Copy the template file
$ cp docker-template.env .env
# Edit the file, add the required variables
$ vim .env
```

## Usage
### In Docker
```sh
$ docker build -t dbc .
$ docker run --rm -it --env-file .env dbc
```

## Resources
- [MS Docs: sing Azure Active Directory with the ODBC Driver - Authenticating with an Access Token](https://docs.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory?view=sql-server-ver15#authenticating-with-an-access-token)
- [StackOverflow: Token-based authentication support for Azure SQL DB using Azure AD auth](https://stackoverflow.com/a/61115563)
- [Medium: Connect to a SQL Database from Python using access token](https://ivan-georgiev-19530.medium.com/connect-to-a-sql-database-from-python-using-access-token-62dcf20c5f5f)
- [Query SQL Database from Python using pyodbc and access token](https://igeorgiev.eu/azure/howto-connect-and-query-sql-database-with-token-using-python-and-pyodbc/)
