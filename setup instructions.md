# Part - I -> Setting up Django
* Install virtualenv
     `sudo pip3 install virtualenv`
* Create a new virtual environment
    `mkdir ~/venv`
    `virtualenv ~/venv/Group-B`
* Activate the virtual environment
    `source ~/venv/Group-B/bin/activate`
* Install django
    `sudo pip install django`

# Part - II -> Using the virtual environment
* To enter the virtual environment, type
    `source ~/venv/Group-B/bin/activate`
* To exit the virtual environment, type
    `deactivate`

# Part - III -> Starting the server
* To start the server, enter the virtual environment, cd into iiticseleave folder, and type
    `python manage.py runserver`
* The website can then be accessed on `localhost:8000` from any web browser
