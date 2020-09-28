# Coding task to find suitable places to eat for team members 


## Setup
Assuming a (new) virtual environment is set up already and activated.  

Designed to run with Python 3.8
```
pip install -r requirements.txt
```
Usage:
```
$ python main.py -h

usage: main.py [-h] [-o OUTPUT] -u USERS -v VENUES

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output json file path 

Required named arguments:
  -u USERS, --users USERS
                        path to json file defining team members food & drink requirements
  -v VENUES, --venues VENUES
                        path to json file outlining food & drink options
```

## TODO
Due to time limitations
* `Places_to_avoid`

After completing the coding exercise for `Places_to_visit`, although I mapped users to their dietary requirements, I realized afterwards, just before submission that I had forgotten to map:
* users to their drinks of choice.


## Execute the script
To run for script to find suitable places to eat:
```
python main.py -u ./input_feeds/users.json -v ./input_feeds/venues.json
```

## Tests

Unit-tests can be run as:
```
python -m pytest -v tests/test_main.py
```
