# Spoiled4you.work

https://sanguine-robot-258820.appspot.com/

## By Yahia Bakour 

### 11/13/2019

## Summary of Project ##

For a while now, I've wanted to build an entire web-app on my own. From idea -> design -> deliver -> deploy. The best idea I had at the time for something new was a web application that would generate spoilers from wikipedia & imdb and would then schedule these spoilers to be sent to an email/phone number. Thus this half-baked project was born !

## Setup Instructions

To run the application locally, clone this repository and do the following:

1. Install Python 3
2. CD into the directory
3. Do pip3 install -r requirements
4. run ./start.sh
5. Create a Config directory within the main directory and add secret keys.  We can email you those.
6. Run 'python3 -m flask run'
7. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
8. Do ‘CTRL+C’ in your terminal to kill the instance.


### Technology

This web application was built using Flask as the backend framework and Jinja-2/HTML/CSS/Javascript/JQuery on the front-end. I debated using a "real" front-end framework but decided that for my first solo project I would use HTML/CSS/Javascript to learn what OG web dev looked like.

For the User Authentication and analytics I used Flask-Login in conjunction with a remote MySQL DB to track user interactions and logins.

For generating spoilers, I used a Wikipedia Python wrapper library and scraped the plot off of the wikipedia post for a given movie (This may not work sometimes, I'm still building the algorithm.)

Currently working on an autocomplete feature using JQuery, Ajax, and flask for generating a list of suggested movies from imdb based off what the user types into the pick-a-movie page.

### Web Hosting

I used Google App Engine on Google Cloud to host our application.  Google App Engine provides an almost no-config deployment option for Python applications, so running it there was straightforward.  It can be accessed at https://sanguine-robot-258820.appspot.com/.



### User Stories / Acceptance Criteria

As a user, I'd like to be able to see a landing page with a CTA button.

As a user, I'd like to be able to see an about us page.

As a user, I'd like to be able to sign up.

As a user, I'd like to be able to login.

As a user, I'd like to be able to login and send a spoiler.

As a user, I'd like to be able to login and see my history of sent spoilers

As a user, I'd like to be able to generate spoilers/plots for the movie i select.\

As a user, I want a clean UI.

As a user, I want to see a 404 page on incorrect URL entry.

### Unit Testing / Manual

In order to make sure the code is free of bugs, we extensively tested additional user stories that involved edge cases and unexpected behaviors.  Some examples include:

* If a user resizes the webpage or views it in a small window, it still renders correctly.
* If a user enters a nonsensical movie, the app still returns a result (sometimes no result, but hey atleast it's not an error)
* If a user incorrectly formats their entry, the app returns a custom error message saying so and prompting them to re-enter.
* If a user enters an invalid URL at our domain, it will display a custom error message.

### Unit Testing / Code

I also implemented some simple unit tests using python's built in library (unittest), we wrote code to unit test for the following:

* Login Page routing
* Load Page routing
* Register Page routing 
* Landing page routing 
* Login Page Scenarios
* Signup Page Scenarios
* Generating Spoiler Scenarios
* AboutUS page routing


### References

* https://codemyui.com/
* https://cloud.google.com/docs/
* https://realpython.com/flask-google-login/
* https://developers.google.com/maps/documentation/geolocation/intro
* https://github.com/alberanid/imdbpy
* https://github.com/goldsmith/Wikipedia
* https://www.w3schools.com/jquery/