# trackwell

## Summary
**trackwell** is an app that allows users to see how their behaviors correlate with their sense of wellness.
It works by having users make daily entries for how long they slept the night before last, exercised yesterday,
and their screen time yesterday. With charts and customized sentences generated based on regression analyses, 
trackwell shows the user the relationship between their lifestyle and sense of wellness.

## About the Developer
Isabella Applen is a Bay Area based software engineer with an educational background in psychology and research 
methods.

## Technologies
### Tech Stack:

+ Python
+ Flask
+ SQLAlchemy
+ PostgreSQL

+ Javascript
+ JQuery
+ HighCharts
+ Jinja
+ Bootstrap
+ HTML
+ CSS


## Features
By pairing behavior data points with their corresponding wellness scores for each day,
and then performing regression analyses on the resulting lists, trackwell is able to determine which behavior best explains
a user's variation in their sense of wellness. Additionally, trackwell analyzes the relationship between behaviors and *next day* sense of wellness. Based on the behavior-wellness relationship that has the highest adjusted r-squared value,
customized sentences are generated to tell the user which behavior is most relevent to their same day sense of wellness and 
which is most relevent to their sense of wellness the following day. These functions examine slope to determine the directionality of the correlation, and uses this information to to inform the user if the behavior is helpful or harmful to their sense of wellness.  
The user can view these insights on the MyStats page, through Jinja-generated statements. This page also shows scatter plot charts for their behavior-wellness relationships, with polynomail trendlines superimposed over the data points. 


If users have other behaviors they would like to track, they can create their own custom variables, and trackwell will conduct the same type of analyses to determine which user-created variable has the strongest relationship with their sense of wellness. 


If the user suspects that they have made an error in one of their entries, they can go to the View All Entries Page and update an entry as they see fit using a form at the bottom of the page. 