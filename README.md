
# Description
LitReview is an app allowing you to request the review of a book or to get access to the books that have already been reviewed. Important note : You only get acces to the books reviewed by your followers. Hence, you first need to follow new users on the follow page.

# Installation : How to set up your local environnement
1. Download the code from this repo
2. Extract it and go to the folder with `cd`
3. Create a new virtual env with `python3 -m venv env`
4. Start the virtual env with `source env/bin/activate`
5. Install the required libraries with `pip3 install -r requirements.txt`
6. Start the server with `python3 manage.py runserver`

The server is now live. You can access the website on the following url: http://127.0.0.1:8000/

# Usage
You need the be logged in to access the application. First, create an account (http://127.0.0.1:8000/registration/signup/) and then log in (http://127.0.0.1:8000/registration/signin/).

You will now have access to the following page : 

 - **My feed** : on this page you have access to the tickets or reviews posted by any of your followers. You can create a new ticket or review from this page.
 - **My posts** : list of all the tickets or reviews that you created. You can edit any of your posts from this page.
 - **My follows/followers** : get a list of your followers and and list of the people you follow. You can follow new users from this page.
 - **Log out** : Log out from the application.
