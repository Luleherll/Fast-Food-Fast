# Fast-Food-Fast
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/Luleherll/Fast-Food-Fast.svg?branch=API)](https://travis-ci.com/Luleherll/Fast-Food-Fast)
[![Maintainability](https://api.codeclimate.com/v1/badges/0a46deab9bc7008a20f7/maintainability)](https://codeclimate.com/github/Luleherll/Fast-Food-Fast/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Luleherll/Fast-Food-Fast/badge.svg?branch=API)](https://coveralls.io/github/Luleherll/Fast-Food-Fast?branch=API)<br/>

Fast-Food-Fast is a food delivery app.<br/>

This API enables the the user to add, update the status and retrieve orders:<br/>

## API ROUTES:
 HTTP Method | Endpoint | Action
-------|-------|-------
 POST | `/api/v1/orders` | For placing orders
 GET | `/api/v1/orders` | For retrieving all orders in the orders list
 GET | `/api/v1/orders/<int:order_id>` | For retrieving one order
 PUT | `/api/v1/orders/<int:order_id>` | For updating the status of one order
