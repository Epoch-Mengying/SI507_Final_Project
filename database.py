# Import statements
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import sys
import csv
from config import *  # go to config.py and change it to yours!

db_connection, db_cursor = None, None

# ---------------------------------------------------------------------
# Database connection, set up, insert
# ---------------------------------------------------------------------

# Write code / functions to set up database connection and cursor here.
def get_connection_and_cursor():
    global db_connection, db_cursor
    if not db_connection:
        try:
            if db_password != "":
                db_connection = psycopg2.connect("dbname = {0} user = {1} password = {2}".format(db_name, db_user, db_password))
                print("Success connecting to database")
            else:
                # note you shouldn't use comma to seperate the argument
                db_connection = psycopg2.connect("dbname = {0} user = {1}".format(db_name, db_user))
                
        except:
            print("Unable to connect to the database. Check server and credentials(config.py).")
            sys.exit(1) #force exit of the program

    if not db_cursor:
        db_cursor = db_connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    
    return db_connection, db_cursor


db_connection, db_cursor = get_connection_and_cursor()


# Write code / functions to create tables with the columns you want and all database setup here.
def set_up_database():
    """ This function helps set up the table with column names. """
####### Note: Use double quotes to make sure the name does not convert to lower case by postgres.

    db_cursor.execute('DROP TABLE IF EXISTS "Restaurants"')
    db_cursor.execute('DROP TABLE IF EXISTS "PriceLevel"')
    db_cursor.execute('DROP TABLE IF EXISTS "Reviews"')
    
    # Table: PriceLevel. 
    # Column: 
        # - id (SERIAL)
        # - price_level (VARCHAR up to 28 chars, UNIQUE)

    db_cursor.execute('CREATE TABLE "PriceLevel" ("id" SERIAL PRIMARY KEY, "price_level" VARCHAR(50) NOT NULL UNIQUE)')
    
    # Table: Reviews
    # Column: 
        # - id (SERIAL)
        # - review_1 (TEXT)
        # - review_2 (TEXT)
        # - review_3 (TEXT)
    db_cursor.execute('CREATE TABLE "Reviews" ("id" SERIAL PRIMARY KEY, "review_1" TEXT NOT NULL UNIQUE, "review_2" TEXT NOT NULL UNIQUE, "review_3" TEXT NOT NULL UNIQUE)')
    
    # Table: Restaurants. Restaurants are stored in lower case, alphabetically.
    # Column: 
        # - id (SERIAL)
        # - restaurant_name (VARCHAR up to 128 chars, UNIQUE)
        # - categories (VARCHAR up to 300 chars)
        # - price_level_id (INTEGER - FOREIGN KEY REFERENCING PriceLevel)
        # - ratings (REAL)
        # - review_count (INTEGER)
        # - longitude (DOUBLE PRECISION)
        # - latitude(DOUBLE PRECISION)
        # - review_id (INTEGER - FOREIGN KEY REFERENCING Reviews)
    db_cursor.execute('CREATE TABLE "Restaurants" ("id" SERIAL PRIMARY KEY, "restaurant_name" VARCHAR(40) NOT NULL UNIQUE, "categories" VARCHAR(300) NOT NULL, "price_level_id" INTEGER REFERENCES "PriceLevel"("id") NOT NULL, "ratings" REAL NOT NULL, "review_count" INTEGER NOT NULL, "longitude" DOUBLE PRECISION NOT NULL, "latitude" DOUBLE PRECISION NOT NULL, "review_id" INTEGER REFERENCES "Reviews"("id") NOT NULL)')
 
    
    # Save 
    db_connection.commit()
    print("Database: Price Level, Reviews, Restaurants have been successfully set up.")


# Write code / functions to deal with CSV files and insert data into the database here.
def insert(connection, cursor, table, data_dict, no_return = True):
    """ Accepts connection and cursor, table name, data dictionary that represents one row, and inserts data into the table."""
    #connection.autocommit = True
    column_names = data_dict.keys()

    if not no_return:
        query = sql.SQL('INSERT INTO "{0}"({1}) VALUES({2}) ON CONFLICT DO NOTHING RETURNING "id"').format(
            sql.SQL(table),
            sql.SQL(', '). join(map(sql.Identifier, column_names)),
            sql.SQL(', ').join(map(sql.Placeholder, column_names))
        )

    else:
        query = sql.SQL('INSERT INTO "{0}"({1}) VALUES({2}) ON CONFLICT DO NOTHING').format(
            sql.SQL(table),
            sql.SQL(', '). join(map(sql.Identifier, column_names)),
            sql.SQL(', ').join(map(sql.Placeholder, column_names))
        )

    sql_string = query.as_string(connection)
    cursor.execute(sql_string, data_dict)

    if not no_return:
        return (cursor.fetchone()["id"])

# ---------------------------------------------------------------------
# Database Helper Function
# ---------------------------------------------------------------------
def get_restaurant_dict(rest_obj, price_level_dict, review_id):
    """ This helper function will convert Restaurant Object into a restaurant dictionanry that can be passed into
    insert() function in order to be inserted into the database.
    
    Args:
      rest_obj: A Restaurant object
      price_leve_dict: A python dictionary that stores eg. key = "$", value = "price_level_id" (many to one)
      review_id: rest_obj's corresponding review id in the Table Reviews
    
    Returns:
      A dictionary that can be passed into insert(). Keys are matched with the table Restaurant column names
    """
    rest_dict = {}
    rest_dict["restaurant_name"] = rest_obj.name
    rest_dict["categories"] = rest_obj.categories
    rest_dict["price_level_id"] = price_level_dict[rest_obj.price]
    rest_dict["ratings"] = rest_obj.ratings
    rest_dict["review_count"] = rest_obj.review_counts
    rest_dict["longitude"] = rest_obj.longitude
    rest_dict["latitude"] = rest_obj.latitude
    rest_dict["review_id"] = review_id
    
    return rest_dict


def get_reviews_dict(review_list):
    review_dict = {}
    review_dict["review_1"] = review_list[0]
    review_dict["review_2"] = review_list[1]
    review_dict["review_3"] = review_list[2]
    return review_dict
    
    
    
    
    
    
    
    
    
    
    
