# Fast-Food-Fast

Fast-Food-Fast is a food delivery app where customers can order food at their convinience.<br/>

# USERS CAN:
>Create an account and login<br/>
>View the menu of all food options<br/>
>Order for food<br/>
>See their pending orders<br/>
>See their order history<br/>
>Logout<br/>

# ADMIN USERS CAN:
>See a list of new orders<br/>
>Accept or decline orders<br/>
>See a list of all pending orders<br/>
>See all completed and declined orders<br/>
>Delete a completed or declined order<br/>
>Add food options to the menu<br/>
>Update a food option on the menu<br/>
>Remove a food option on the menu<br/>
>Promote normal users to admins<br/>
>Switch to a normal user dashboard<br/>

[![Website perso.crans.org](https://img.shields.io/website-up-down-green-red/http/perso.crans.org.svg)](http://perso.crans.org/)<br>
Here is a link to a fully functional app:<br/>
## https://lule-foods.herokuapp.com/

# Fast-Food-Fast API

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/Luleherll/Fast-Food-Fast.svg?branch=develop)](https://travis-ci.com/Luleherll/Fast-Food-Fast)
[![Maintainability](https://api.codeclimate.com/v1/badges/0a46deab9bc7008a20f7/maintainability)](https://codeclimate.com/github/Luleherll/Fast-Food-Fast/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Luleherll/Fast-Food-Fast/badge.svg?branch=develop)](https://coveralls.io/github/Luleherll/Fast-Food-Fast?branch=develop)

Here is the link for the API hosted on Heroku with Swagger API documentation to demo the API:<br/>
# https://lule-persistent.herokuapp.com/

## API ROUTES:
 HTTP Method | Endpoint | Action
-------|-------|-------
 POST | `/api/v2/auth/signup` | For registering new users
 POST | `/api/v2/auth/login` | For looging in users
 POST | `/api/v2/auth/admin` | For promoting normal users to admin role
 POST | `/api/v2/menu` | For adding new food item to the menu
 POST | `/api/v2/users/orders` | For placing orders
 GET | `/api/v2/users/orders` | For getting user's pending orders
 GET | `/api/v2/users/history` | For getting user order history
 GET | `/api/v2/orders` | For retrieving all orders in the orders list
 GET | `/api/v2/menu` | For getting the menu
 DELETE | `/api/v2/menu` | Removing food option from the menu
 GET | `/api/v2/orders/<int:order_id>` | For retrieving one order
 PUT | `/api/v2/orders/<int:order_id>` | For updating the status of one order
 PUT | `/api/v2/menu/<string:name>` | For updating specific food option on the menu
