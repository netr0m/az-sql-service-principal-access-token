import struct
import os

import pyodbc
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential

# MSAL
TENANT_ID = os.getenv("AD_TENANT_ID")
CLIENT_ID = os.getenv("AD_CLIENT_ID")
AUTHORITY = f"https://login.microsoftonline.com/"
CLIENT_SECRET = os.getenv("AD_CLIENT_SECRET")
SCOPE = "https://database.windows.net/.default"

# ODBC
SQLDB_SERVER = os.getenv("SERVER")
SQLDB_PORT = int(os.getenv("PORT", 1433))
SQLDB_DB = os.getenv("DB")

DRIVER = "{ODBC Driver 18 for SQL Server}"
SERVER = f"tcp:{SQLDB_SERVER},{SQLDB_PORT}"
DATABASE = f"{SQLDB_DB}"
SQL_COPT_SS_ACCESS_TOKEN = 1256
CONNSTR = f"Driver={DRIVER};Server={SERVER};Database={DATABASE}"


def prepare_token(access_token: str) -> bytes:
    exptoken = b""
    for i in bytes(access_token, "UTF-8"):
        exptoken += bytes({i})
        exptoken += bytes(1)
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    return tokenstruct


def connect(tokenstruct: bytes) -> pyodbc.Connection:
    return pyodbc.connect(CONNSTR, attrs_before={ SQL_COPT_SS_ACCESS_TOKEN: tokenstruct })


def execute_query(con: pyodbc.Connection) -> any:
    with con.cursor() as cur:
        cur.execute("SELECT getdate()")
        return cur.fetchone()


def retrieve_access_token() -> str:
    if TENANT_ID and CLIENT_ID and CLIENT_SECRET:
        print("Using service principal")
        credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        return credentials.get_token(SCOPE).token
    elif TENANT_ID and CLIENT_ID:
        # Cannot be run in docker, as it requires the ability to launch a browser
        raise NotImplementedError("Using a service principal with delegated access is not currently functioning.")
        # credentials = InteractiveBrowserCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, redirect_uri="http://localhost:8000")
        # return credentials.get_token(SCOPE).token
    else:
        raise EnvironmentError("Missing required environment variables for Azure AD authentication")


if __name__ == "__main__":
    token = retrieve_access_token()
    tokenstruct = prepare_token(token)
    con = connect(tokenstruct)
    row = execute_query(con)
    print(row[0])
