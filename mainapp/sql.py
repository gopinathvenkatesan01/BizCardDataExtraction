import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import streamlit as st
import sqlalchemy
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    MetaData,
    select,
    String,
    Text,
    update,
    delete,
)
import pandas as pd
import uuid


database_url = "postgresql+psycopg2://postgres:admin@localhost:5432/bizcard"
engine = create_engine(database_url, echo=False)
schema = "bizcard"


def psql_client():
    try:
        connection = psycopg2.connect(
            host="localhost", user="postgres", password="admin", database="bizcard"
        )
        return connection
    except Exception as e:
        print(e)


def init():
    create_database("bizcard")


def create_database(schema):
    print("creating schema:>>>>")
    try:
        conn = psql_client()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        sqlQuery = (
            "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"
        )
        # Execute the query statement
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        # Extract database names from the fetched rows
        database_names = [db[0] for db in rows]
        # Check if the schema exists in the fetched database names
        if schema in database_names:
            st.toast("Database '{}' Already Exists.".format(schema))
        # create schema
        else:
            db_crt_qry = "create schema " + schema + ";"
            cursor.execute(db_crt_qry)
            # Executing tables script
            with open("script.sql", "r") as file:
                sql = file.read()
                # Execute the SQL script
                cursor.execute(sql)
            conn.commit()
            st.toast("Table Created Successfully")
    except (psycopg2.Error, Exception) as e:
        # Handle database-related errors
        st.write("An error occurred:", e)
    finally:
        # Close cursor and connection in the 'finally' block
        if "connection" in locals():
            # Close the cursor
            cursor.close()
            # Close the connection
            conn.close()


def build_user_details_table():

    table_name = "user_details"

    # Create a metadata instance
    metadata = MetaData(schema=schema)

    # Define the table structure
    user_details_table = Table(
        table_name,
        metadata,
        Column("bizcardky", String(length=255)),
        Column("company_name", String(length=225)),
        Column("card_holder", String(length=225)),
        Column("designation", String(length=225)),
        Column("mobile_number", String(length=50)),
        Column("email", Text),
        Column("website", Text),
        Column("area", String(length=225)),
        Column("city", String(length=225)),
        Column("state", String(length=225)),
        Column("pin_code", String(length=10)),
        autoload_with=engine,
        extend_existing=True,
    )

    return user_details_table


def saveCardData(data):
    # Fetch existing data from the database
    with engine.connect() as connection:
        user_details_table = build_user_details_table()
        query = select(user_details_table)
        existing_data = pd.read_sql(query, connection)

    unique_columns = ["company_name", "card_holder", "mobile_number","email"]

    # Validate and filter new data to remove duplicates
    mask = data.apply(
        lambda row: any(
            existing_data[unique_col].eq(row[unique_col]).any()
            for unique_col in unique_columns
        ),
        axis=1,
    )

    filtered_data = data[~mask]
    
    try:
        if not filtered_data.empty:
            filtered_data["bizcardky"] = uuid.uuid4()
            filtered_data.to_sql(
                "user_details",
                engine,
                if_exists="append",
                index=False,
                dtype={
                    "bizcardky": sqlalchemy.types.VARCHAR(length=225),
                    "company_name": sqlalchemy.types.VARCHAR(length=225),
                    "card_holder": sqlalchemy.types.VARCHAR(length=225),
                    "designation": sqlalchemy.types.VARCHAR(length=225),
                    "mobile_number": sqlalchemy.types.String(length=50),
                    "email": sqlalchemy.types.TEXT,
                    "website": sqlalchemy.types.TEXT,
                    "area": sqlalchemy.types.VARCHAR(length=225),
                    "city": sqlalchemy.types.VARCHAR(length=225),
                    "state": sqlalchemy.types.VARCHAR(length=225),
                    "pin_code": sqlalchemy.types.String(length=10),
                },
                schema=schema,
            )
            st.toast("Data Successfully Uploaded")
        else:
            st.toast("Card data already exists")

    except Exception as e:

        st.error(f"An error occurred: {e}")


def getuserData():
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = [
        "bizcardky",
        "company_name",
        "card_holder",
        "designation",
        "mobile_number",
        "email",
        "website",
        "area",
        "city",
        "state",
        "pin_code",
    ]
    try:
        cursor.execute("""SELECT *  FROM bizcard.user_details;""")
        tuples_list = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(tuples_list, columns=coluumn_names)
        return df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()


# update data
def update_database(edited_data, uuid_mapping, connection):
    # Merge edited data with uuid_mapping to get UUIDs back
    updated_data = edited_data.join(uuid_mapping)
    for index, row in updated_data.iterrows():
        user_details_table = build_user_details_table()
        stmt = (
            update(user_details_table)
            .where(user_details_table.c.bizcardky == row["bizcardky"])
            .values(
                company_name=row["company_name"],
                card_holder=row["card_holder"],
                designation=row["designation"],
                mobile_number=row["mobile_number"],
                email=row["email"],
                website=row["website"],
                area=row["area"],
                city=row["city"],
                state=row["state"],
                pin_code=row["pin_code"],
            )
        )
        connection.execute(stmt)
    connection.commit()


# delete data
def delete_rows_from_db(rows_to_delete, connection):
    for row in rows_to_delete:
        user_details_table = build_user_details_table()
        stmt = delete(user_details_table).where(user_details_table.c.bizcardky == row)
        connection.execute(stmt)
    connection.commit()


def delete_data(deleted_data, uuid_mapping):
    if deleted_data:
        uuids = uuid_mapping[["bizcardky"]].copy()
        uuids.index = uuids.index - 1
        data_to_delete = uuids.loc[deleted_data, "bizcardky"].tolist()
        with engine.connect() as connection:
            delete_rows_from_db(data_to_delete, connection)
            st.toast("Data Deleted Successfully")


def saveData(edited_data, uuid_mapping):
    with engine.connect() as connection:
        update_database(edited_data, uuid_mapping, connection)
        st.toast("Database Updated Successfully")
