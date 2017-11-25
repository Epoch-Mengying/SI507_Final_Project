# SI507 Final Project: Invesitigating Coursera's online Machine Learning Class


> Machine learning courses focus on creating systems to utilize and learn from large sets of data. Topics of study include predictive algorithms, natural language processing, and statistical pattern recognition (from Coursera topic description).


## Goal of the Project

The goal of the project is to use Python to web scrape the machine learning courses from Coursera. 

## Data Source
Coursera homepage >> Catelog >> Data Science >> Machine Learning

Machine learning module is one of the three modules(Data Analysis, Michine Learning, Probabilities and Statistics)under Data Science category on Coursera. I chose this site becuase I myself have been a great beneficiary of the online open education and my academic focus is on machine learning. 

The web source of the data is:

* Machine learning course catelog: https://www.coursera.org/browse/data-science/machine-learning?languages=en
* Specialization course homepage: https://www.coursera.org/specializations/{specialization_name}
   * eg. Deep Learning Specialization https://www.coursera.org/specializations/deep-learning



## Outcome

### CSV files

There are two csv files(potentially more, depends on the cnumber of specialization course) that contain the information we have scraped. Each csv's column names are provided below.

* machine_learning_classes.csv
  * course_title: the name of the course
  * institution: university/other agencies that provided/taught the course
  * num_courses_in_splz: number of courses in the specialization. If the course is not a specialization course(ie. a single course), the column will be left blank. Specilization means 
  * course_page_URL: the website link that leads to the course homepage.
  
--> Data Source: https://www.coursera.org/browse/data-science/machine-learning?languages=en

**Note: this course list should not contain duplicate courses as what is currently presented on the website. In other words, if one course is already in one specialization, it should not be listed as a seperate class in this list.**

* {Specialization_name}.csv
   * course_name: course names which are listed in the learning path order
   * num_weeks: how many weeks it should take to finish the course
   * num_hours_per_week:  how many hours it should take to learn the material per week
   * about: course description

--> Data Source: https://www.coursera.org/specializations/{specialization}


### Database

There will be three tables stored in the database:

* Table1: Machine Learning Courses
  * id: PRIMARY KEY
  * course title
  * institution id: FOREIGN KEY points to Table3 Institutions(id)
  * specialization id:  FOREIGN KEY points to Table2 Specialization(id)
  * number of courses
  * course page URL
  
  
* Table2: Specialization
  * id: PRIMARY KEY
  * course name
  * number of weeks
  * hours per week
  * about
  
* Table3: Institutions
  * id: PRIMARY KEY
  * institution
  
### An Excel Workbook
This workbook nicely incorporates all the information I gained in the project. It's user friendly and can act as a course catelog guide for you to play with. You can use this workbook to find the right machine learning course to take and easily navigate to that site!

The workbook has: 
* a list of all machine learning courses on Coursera
* different specialization courses with detailed course descriptions
* URL that you can click on and directly navigates to the course homepage

    





