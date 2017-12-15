# SI507 Final Project: Ann Arbor's Best Restaurants from Yelp


>  "Very very special brunch at local! It's definitely worth coming on new year's day!" 
                                                             --- A Customer Review for The Boutique Cafe & Lounge from Yelp


## Goal of the Project

The goal of the project is to use python to get data from Yelp API on Ann Arbor's restaurants information(**Note: only 40 restaurants can be returned at this point.**) and store the data into database for query/management. There will also be an interactive map built by Tableau and HTML for users to interact with. 

## Data Source: Yelp

Yelp is an application that provides restaurants' information/reviews. It is supported by multiple languages and is widely used in many countries such as the U.S. and Japan. After users pick a location(and other possible criteria), Yelp will return satisfying restaurants search results. 

Yelp @ Ann Arbor: https://www.yelp.com/search?find_desc=&find_loc=Ann+Arbor%2C+MI&ns=1

Tool to get the data: Yelp Fusion API, which uses OAuth 2.0 as Authentication.
  * API documentation homepage: https://www.yelp.com/developers/documentation/v3/get_started
  * Search API documentation: https://www.yelp.com/developers/documentation/v3/business_search
  * Reviews API documentation: https://www.yelp.com/developers/documentation/v3/business_reviews

**IMPORTANT UPDATES: From December 8, 2017, Yelp simplifies the API process and change from using OAuth 2.0 to API key. However, this code will still work until Yelp completely stops using OAuth 2.0 starting March 1, 2018.**

## Outcome

We will get information on 40 best restaurants in Ann Arbor ordered by some sorting function by Yelp(taking both review counts and ratings into account), plus the corresponding 3 review extracts for each restaurant we retrieved.

### CSV files

There are two csv files that contain the information we have gained. Each csv's column names are provided below.

* restaurants.csv (saves restaurant basic information on name, category, rating, price level and location)
  * restaurant_id: the registered id of the restaurant
  * restaurant_name: the name of the restaurant
  * category: which categories the restaurant belongs to, eg. Coffee & Tea. can be multiple categories. stored in a list.
  * price_leve: range from $ to $$$$
  * ratings: range from 1 to 5, on a 1/2 interval
  * review_counts: total number of reviews
  * state: the location of the restauant
  * city
  * street_address
  * latitude
  * longitude
  
--> Search API documentation: https://www.yelp.com/developers/documentation/v3/business_search


* reviews.csv
   * restaurant_id: the registered id of the restaurant
   * reiview_1: one review of the customer
   * review_2: one review of the customer
   * review_3: one review of the customer

--> Reviews API documentation: https://www.yelp.com/developers/documentation/v3/business_reviews


**Note: This file only stores the three reviews extract returned by the API endpoints. At this time, the API does not return restaurants without any reviews.** 


### Database

There will be three tables stored in the database:

* Table1: Restaurants
  * id: PRIMARY KEY
  * restaurant_name
  * price_level
  * ratings
  * reviews_count
  * logitude
  * latitude
  * category id: FOREIGN KEY points to Table2 Category(id)
  * review id:  FOREIGN KEY points to Table3 Reviews(id)
  
  
* Table2: PriceLevel
  * id: PRIMARY KEY
  * price_level
  
* Table3: Reivews
  * id: PRIMARY KEY
  * review_1
  * review_2
  * review_3
  
  
### An Interactive Map

Unlike database, this interactive map allows the users to interact with 40 restaurants' information we gained in this project! 

Map is generated by Tableau, which will be displayed on the web. It shows 40 best restaurants on Yelp in Ann Arbor. User can click on point on the map to see the corresponding restaurants'information. Point size indicates the number of ratings, with bigger size meaning more number of reviews, and point color indicates the average rating.

Have fun!


## Instructions
The project is a bit completed. Here's **how to run the code**!
#### Step 1: Create your own application on Yelp!
 [1] Go to Yelp API documentation: https://www.yelp.com/developers/documentation/v3 <br/>
 [2] Click on Create App at left under General <br/>
 [3] Check your client_ID and client_secret here: https://www.yelp.com/developers/v3/manage_app <br/>
     Note, as this code uses OAuth 2.0, your don't need to worry about API key! <br/>
 [4] Fill in your client_ID and client_secret in **secret_data_sample.py** and rename it to **secret_data.py**

#### Step 2: Changing the database user name to yours!
 [1] Open **config.py** and change it to your own user name! You don't need to change the database name.<br/>
 [2] Make sure you have all the database pre-installs.
 
#### Step 3: Create a virtual environment and pip install everything!
 [1] Create a virtual environment named "venv" and activate it by <br/>
```
 virtualenv --python=python3 venv
 source venv/bin/activate
```
 [2] Pip install the required libraries from **requirements.txt** using <br/>
```
 pip install -r requirements.txt
```
 #### Step 4: Run the main code inside your virtual environment!
 ```
 python SI507F17_finalproject.py
```

 #### [Optional] Run the test case inside your virtual environment!
 ```
 python SI507F17_finalproject_tests.py
```

 #### What you will see on your console after running the main code ...
 You will see something like this:
 
 ![sample console output](https://github.com/Epoch-Mengying/SI507_Final_Project/blob/master/Screenshot_Console.png)
 
 Basically the message is telling you what the code is doing at each step! After reading this, you will have a clear idea of what's going on in the code!
 
 #### What you will get after running the main code...
 * cached json files
    * creds.json:  a json file containing your cached credentials
    * cache_contents.json: a json file containing your cached restaurants information. 
    * reviews.json: a json file containing your cached restaurants' reviews information.
  
 * csv files
    * restaurants.csv
    * reviews.csv
  
 As an example, you can see what I got for all the json and csv files in my repo(except creds.json)!
 #### What you can play with ...
 * **visualization.html**   <br/>
  You can open this file in your browser and see the interactive map I have built using the restaurants' data we got! <br/>
  You will see something awesome like this: ![sample visualization page](https://github.com/Epoch-Mengying/SI507_Final_Project/blob/master/Screenshot_InteractionMap.png)
  

#### Other files that I didn't mention:
 * restaurants_yelp.twb   <br/>
  This is the original Tableau workbook I created to show the interactive map. If you are a data visualization person, feel free to play with it!
  
 * sample_3restaurants.py   <br/>
 This is the sample data format retrieved from Yelp Search API. This file is for test only.
 
 * database.py   <br/>
 This file deals with all the postgres and is imported in our main code file SI507F17_finalproject.py. So you don't need to worry about it!






