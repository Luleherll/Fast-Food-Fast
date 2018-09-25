# Fast-Food-Fast
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/Luleherll/Fast-Food-Fast.svg?branch=revision)](https://travis-ci.com/Luleherll/Fast-Food-Fast)
[![Coverage Status](https://coveralls.io/repos/github/Luleherll/Fast-Food-Fast/badge.svg?branch=revision)](https://coveralls.io/github/Luleherll/Fast-Food-Fast?branch=revision)

Fast-Food-Fast is a food delivery app.<br/>

This API enables the the user to add, update the status and retrieve orders:<br/>

Here is the link for the API hosted on Heroku:<br/>
# https://lule-fast-food.herokuapp.com/

## API ROUTES:
 HTTP Method | Endpoint | Action
-------|-------|-------
 POST | `/api/v1/orders` | For placing orders
 GET | `/api/v1/orders` | For retrieving all orders in the orders list
 GET | `/api/v1/orders/<int:order_id>` | For retrieving one order
 PUT | `/api/v1/orders/<int:order_id>` | For updating the status of one order
