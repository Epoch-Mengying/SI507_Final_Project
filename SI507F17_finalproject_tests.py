import unittest
import json
from SI507F17_finalproject import *

class Get_Data_Test(unittest.TestCase):
    
    def setUp(self):
        self.creds = open("creds.json", "r")
        self.rest = open("cache_contents.json", "r")
        self.rev = open("reviews.json", "r")
        
    def test_creds_json_exist(self):
        self.assertTrue(self.creds.read())
    
    def test_rest_json_exist(self):
        self.assertTrue(self.rest.read())
        
    def test_rev_json_exist(self):
        self.assertTrue(self.rev.read())
        
    def test_number_of_restaurants(self):
        self.assertEqual(CACHE_DICTION["total"], 40)
    
    def tearDown(self):
        self.creds.close()
        self.rest.close()
        self.rev.close()    


class CSV_Files_Test(unittest.TestCase):
    
    def setUp(self):
        self.rev = open("reviews.csv", "r")
        self.rest = open("restaurants.csv", "r")

        
    def test_csv_files_exist(self):
        self.assertTrue(self.rest.read())
        self.assertTrue(self.rev.read())

    def test_review_content(self):
        self.assertEqual(self.rev.readline(), "restaurant_id,review_1,review_2,review_3\n")
        self.assertTrue(self.rev.readline())
    
    def test_restaurant_content(self):
        self.assertEqual(self.rest.readline(), "restaurant_id,restaurant_name,categories,price_level,ratings,review_counts,state,city,street_address,latitude,longitude\n")
        self.assertTrue(self.rest.readline())
        
    def tearDown(self):
        self.rest.close()
        self.rev.close()
        

class Restaurant_Class_Test(unittest.TestCase):
    
    def setUp(self):
        self.f = open("sample_3restaurants.py", "r")
        rest_json = self.f.read()
        self.restaurants = json.loads(rest_json)["businesses"] # a list of 3 restaurants
        self.samp_rest = Restaurant(self.restaurants[0])
        self.f.close()
        
    def test_restaurant_constructor(self):
        self.assertIsInstance(self.samp_rest.name, str)
        self.assertIsInstance(self.samp_rest.street_address, str)

    def test_restaurant_contains(self):
        self.assertTrue("Casablanca" in self.samp_rest)
        
    def test_repr(self):
        self.assertEqual("<A Restaurant Object: 'name':Casablanca, 'price':$$, ratings: 4.5, city: Ypsilanti, address:2333 Washtenaw Rd>",repr(self.samp_rest))
        


class List_Dictionary_Test(unittest.TestCase):
    
    def test_ann_arbor_restaurants(self):
        self.assertIsInstance(ann_arbor_restaurants, list)
        
    def test_price_level_id(self):
        self.assertIsInstance(price_level_id, dict)
        self.assertTrue(price_level_id)  # not empty
    
    def test_restaurant_inst(self):
        self.assertIsInstance(ann_arbor_restaurants[0], Restaurant)
        
    def test_price_level(self):
        self.assertEqual(len(price_level_list), 4)
    
    def test_businesses_list(self):
        self.assertIsInstance(businesses, list)



    
if __name__ == '__main__':
    unittest.main(verbosity=2)