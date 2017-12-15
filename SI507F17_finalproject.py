import json
import os
import os.path
import requests
import sys
import csv
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from database import *
import secret_data # Go to secret_data_sample.py and follow the instructions!


#-------------------------------------------------------------------------------
# OAuth 2.0 Yelp API Client Info: based on sample code from Yelp: 
# https://github.com/Yelp/yelp-fusion/tree/master/fusion/python
#-------------------------------------------------------------------------------

CLIENT_ID = secret_data.client_ID
CLIENT_SECRET = secret_data.client_secret
i = 3
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/{id}'  # id: Business ID
REVIEW_PATH = BUSINESS_PATH + '/reviews' # inside BUSINESS_PATH, id: Business ID
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# for debug purpose:
SEARCH_LIMIT = 41


# Functions for OAuth Process
def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token
    
def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()
    

# Use above two functions to request data
def search_api(bearer_token, location = "Ann Arbor", term = "restaurants", limit = SEARCH_LIMIT):
    """Query the Search API by a search term and location. The result is sorted by weighted rating.

        Args:
            location (str): The search location passed to the API. By default, it's Ann Arbor.
            term (str): The search key word passed to the API. By default, it's restaurants.
            limit: The maximum of number of results returned by API is 50.
            
        Returns:
            dict: The JSON response from the request. Sorted by adjusted rating.
    """
    params = {
        'location': location,
        'term': term,
        'limit':limit,
        'sort_by': 'rating'    
    }
    
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params = params)
    
def reviews_api(bearer_token, id):
    """Query the Reviews API by business id.

        Args:
            bearer_token: can be obtained by above function: obtain_bearer_token(host, path)
            id: Business ID can be found from search API.
            
        Returns:
            dict: The JSON response from the request. Include up to 3 reviews.
    """
    review_full_path = REVIEW_PATH.format(id = id) 
    return request(API_HOST, review_full_path, bearer_token)
    

#-------------------------------------------------------------------------------
# CACHE FUNCTION SETUP
#-------------------------------------------------------------------------------
# Set Cache Functions: Writing data to cache file.
def set_in_cache(dict_data, cache_file_name):
    """ This is a general function can be used to write any cached data onto any files user specifies.
    
    Args:
       dict_data: to be cached data. Should be a dictionary.
       cache_file_name: the name of the file user wants to write on.
    
    Returns:
       dict_data itself
    
    Modifies:
       Upon execute, this will write data on the cache file.
    
    """
    print("Getting new data and Setting cache file in {}...".format(cache_file_name))
    
    with open(cache_file_name, 'w') as cache_file:
        cache_json = json.dumps(dict_data)
        cache_file.write(cache_json)

    return dict_data
    

# Get data from cache file or API
def get_data(cache_file_name, identifier = "restaurants", refresh = "No", credential = None, cache = None):
    """ If the data is in the cache file, retrieve from the corresponding cache file, otherwise retrieve data
    from API and set the data into cache file. The function also allows to refresh the search result by setting refresh to "Yes".
    
    Args:
       identifier: the data you want to get. It can be "credentials" or "restaurants" or "reviews". By default, it will get restuarants data.
       cache_file_name: the name of the cache file
       refresh: whether to refresh searching the data. If set to "Yes", it will wipe out the cached file and retrieve the data
                from API and save the new data into the cache file.
       credential: if identifier is "restaurants" or "reviews", you must supply credential
       cache: if identifier is "reviews", you must supply credential
    
    Returns:
       data_diction: cached data as a dictionary
    
    Modifies:
       If the data is not in the cache file, it will be written onto the cache file.
    
    """ 
    # Sanity check for identifier:
    if (identifier not in ("credentials", "restaurants", "reviews")):
        print("**Error: identifier not accepted in function get_data()")
        exit()
    
    if(refresh == "No"):
        # Load the data from cache file
        try:
            print("Getting data from {}...".format(cache_file_name))
            with open(cache_file_name, 'r') as cache_file:
                cache_json = cache_file.read()
                data_diction = json.loads(cache_json)
        except:
            print("No contents found.")
            data_diction = {}
    
        # If not in the cache file, get data from API and set into cache
        if(identifier == "credentials" and not data_diction):
            # get bearer_roken
            bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
            bearer_token_dict = {"token": bearer_token}
            
            # set in cache file
            data_diction = set_in_cache(dict_data = bearer_token_dict, cache_file_name = cache_file_name)
    
        if(identifier == "restaurants" and not data_diction):
            # sanitory check for availability of credentials' data
            if not credential:
                print ("**Error: Obtain your credentials first and retreive restaurants data.")
                exit()
            # get the data using CREDS_DICTION
            search_result = search_api(credential["token"])
            
            # set in cache file
            data_diction = set_in_cache(dict_data = search_result, cache_file_name = cache_file_name)
            
        if(identifier == "reviews" and not data_diction):
            # sanitory check for availability of credentials' data and restaurant data
            if not credential or not cache:
                print ("**Error: Obtain your credentials and restaurants data first and retreive reviews data.")
                exit() 
            # save all restaurant id in list
            ids = []
            businesses = cache["businesses"]
            for business in businesses:
                ids.append(business["id"])
            # get the data using CREDS_DICTION and ids
            review_result = {} # a dictionary with key = restaurant_id, value = a list of up to 3 reviews.
            for id in ids:
                review_list = []
                result = reviews_api(credential["token"], id) # search that restaurant's review
                for one_review in result["reviews"]:
                    review_list.append(one_review["text"]) # extract only the text part and append it to review_list for that restaurant
                review_result[id] = review_list # save it into review_result    
                   
            # set in cache file
            data_diction = set_in_cache(dict_data = review_result, cache_file_name = cache_file_name)
    
    elif(refresh == "Yes"):
        if(identifier == "credentials"):
            if(os.path.isfile(cache_file_name)):
                # clear cache file
                os.remove(cache_file_name)
            
            # get bearer_roken
            bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
            bearer_token_dict = {"token": bearer_token}
            # set in cache file
            data_diction = set_in_cache(dict_data = bearer_token_dict, cache_file_name = cache_file_name)
    
        if(identifier == "restaurants"):
            if(os.path.isfile(cache_file_name)):
                 # clear cache file
                 os.remove(cache_file_name)
            # sanitory check for availability of credentials' data
            if not credential:
                print ("**Error: Obtain your credentials first and retreive restaurants data.")
                exit()
            # get the data
            search_result = search_api(credential["token"])
            
            # set in cache file
            data_diction = set_in_cache(dict_data = search_result, cache_file_name = cache_file_name)
            
        if(identifier == "reviews"):
            if(os.path.isfile(cache_file_name)):
                 # clear cache file
                 os.remove(cache_file_name)
             
            # sanitory check for availability of credentials' data and restaurant data
            if not credential or not cache:
                print ("**Error: Obtain your credentials and restaurants data first and retreive reviews data.")
                exit() 
            # save all restaurant id in list
            ids = []
            businesses = cache["businesses"]
            for business in businesses:
                ids.append(business["id"])
            # get the data using CREDS_DICTION and ids
            review_result = {} # a dictionary with key = restaurant_id, value = a list of up to 3 reviews.
            for id in ids:
                review_list = []
                result = reviews_api(credential["token"], id) # search that restaurant's review
                for one_review in result["reviews"]:
                    review_list.append(one_review["text"]) # extract only the text part and append it to review_list for that restaurant
                review_result[id] = review_list # save it into review_result    
                   
            # set in cache file
            data_diction = set_in_cache(dict_data = review_result, cache_file_name = cache_file_name)
    
    else:
         print ("**Error: Bad value for refresh parameter in function get_data()")
                 
        
    return data_diction

    
#-------------------------------------------------------------------------------
# Write CSV Files
#-------------------------------------------------------------------------------
def write_restaurants_file(restaurants_list, filename):
    """Write the restaurants' informatino on csv file

        Args:
            restaurants_list: a list of restaurants, with each item represented by Restaurant object
            filename: the file to be writte on
            
        Returns:
            None
       
        Modifies:
            the file with filename
    """
    with open(filename,"w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["restaurant_id", "restaurant_name", "categories", "price_level", "ratings", "review_counts", "state", "city", "street_address", "latitude", "longitude"])
        
        for restaurant in restaurants_list:
            csv_writer.writerow([restaurant.id, restaurant.name, restaurant.categories, restaurant.price, restaurant.ratings, restaurant.review_counts, restaurant.state, restaurant.city, 
            restaurant.street_address, restaurant.latitude, restaurant.longitude])
            
    print ("Writing restaurants'information on {}...".format(filename))


def write_reviews_file(reviews_dict, filename):
    """Write the restaurants' informatino on csv file

        Args:
            reviews_dict: a dictionary of reviews, with each item represented by key = restaurant_id, value = list of reviews
            filename: the file to be writte on
            
        Returns:
            None
       
        Modifies:
            the file with filename
    """
    with open(filename,"w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["restaurant_id", "review_1", "review_2", "review_3"])
        
        for item in reviews_dict:
            reviews_list = reviews_dict[item]
            csv_writer.writerow([item, reviews_list[0], reviews_list[1], reviews_list[2]])
            
    print ("Writing restaurants' reviews on {}...".format(filename))
    
    
    
           
#-------------------------------------------------------------------------------
# Class Definition
#-------------------------------------------------------------------------------
class Restaurant(object):
    def __init__(self, rest_obj):
        self.id = rest_obj["id"]
        self.name = rest_obj["name"]
        self.categories = [] # a restaurant can have multiple categories
        for item in rest_obj["categories"]:
            self.categories.append(item["title"]) 
        self.price = rest_obj["price"]
        self.ratings = rest_obj["rating"]
        self.review_counts = rest_obj["review_count"]
        self.state = rest_obj["location"]["state"]
        self.city = rest_obj["location"]["city"]
        self.street_address = rest_obj["location"]["address1"]
        self.latitude = rest_obj["coordinates"]["latitude"]
        self.longitude = rest_obj["coordinates"]["longitude"]
        
    
    def __repr__(self):
        return "<A Restaurant Object: 'name':{}, 'price':{}, ratings: {}, city: {}, address:{}>".format(self.name, self.price, self.ratings, self.city, self.street_address)
        
    
    def __contains__(self, name):
        return name in self.name
               

#-------------------------------------------------------------------------------
# Main Function
#-------------------------------------------------------------------------------

#if __name__ == '__main__':
print ("**Process started**")
# Check if client_id and client_secret has been filled
if not CLIENT_ID or not CLIENT_SECRET:
    print("Please provide Client ID and Client SECRET in secret_data_sample.py")
    exit()

# Set up for cache file name
CREDS_CACHE_FNAME = "creds.json" # a cache file to save the credentials, ie, all the tokens
CACHE_FNAME = "cache_contents.json" # a cache file to save the returned data on Ann Arbor's restaurants
REVIEWS_FNAME = "reviews.json" # a cache file to save the reviews on Ann Arbor's restaurants


# Get credentials data, restaurants data and reviews data
CREDS_DICTION = get_data(CREDS_CACHE_FNAME, identifier = "credentials", refresh = "No") # a python dictionary to store credential data

CACHE_DICTION = get_data(CACHE_FNAME, identifier = "restaurants", refresh = "No", credential = CREDS_DICTION) # a python dictionary to store  restaurants data

REVIEWS_DICTION = get_data(REVIEWS_FNAME, identifier = "reviews", refresh = "No", credential = CREDS_DICTION, cache = CACHE_DICTION) # a python dictionary to store reviews data 


# Create restaurant object for each restaurant retrieved in CACHE_DICTION, and save all in a list
ann_arbor_restaurants = []
businesses = CACHE_DICTION["businesses"]
for business in businesses:
    rest_obj = Restaurant(business)
    ann_arbor_restaurants.append(rest_obj)

# Write each restaurant's information on restaurants.csv file
REST_CSV_FNAME = "restaurants.csv"
write_restaurants_file(restaurants_list = ann_arbor_restaurants, filename = REST_CSV_FNAME)

# Write each restaurant's reviews on reviews.csv file
REV_CSV_FNAME = "reviews.csv"
write_reviews_file(reviews_dict = REVIEWS_DICTION, filename = REV_CSV_FNAME)


# Save all the data into the database 
# Set up database
print("Connecting to the database...")  
set_up_database()

# Save to Table PriceLevel
price_level_list = ["$", "$$", "$$$", "$$$$"]
price_level_id = {} # a python dictionary that stores eg. key = "$", value = "price_level_id"
print ("Inserting to Table PriceLevel...")
for price in price_level_list:
    price_dict = {}
    price_dict["price_level"] = price 
    price_level_id[price] = insert(db_connection, db_cursor, "PriceLevel", price_dict, no_return = False)

# Save to Table Reviews & Table Restaurant
print ("Inserting to Table Reivews and Restaurant...")
for restaurant in ann_arbor_restaurants:
    # Insert to Table Reviews first
    review_dict = get_reviews_dict(REVIEWS_DICTION[restaurant.id])
    review_id = insert(db_connection, db_cursor, "Reviews", review_dict, no_return = False)
    
    # Insert to Table Restaurant
    rest_dict = get_restaurant_dict(restaurant, price_level_id, review_id)
    insert(db_connection, db_cursor, "Restaurants", rest_dict)

# Save all the work for database
db_connection.commit()


print("Total Restaurants: ", CACHE_DICTION["total"])
print('----------------')
print('Process Completed!')