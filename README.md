# Get Token Service

This project is a simple Flask server that will act as a trusted authentication server.

**_WARNING:  Do not share this code outside of ThoughtSpot!  It contains login info to a dev server._**

Calls to the server are in the form of `https://<URL>:5000/gettoken/<username>`

## Python Dependencies
* Python 3 (virtual environment recommended)
* flask
* flask_cors
* requests

## Notes

* This server talks to the embed-1-do-not-delete.thoughtspotdev.cloud server using the tsadmin login.
If the server or login change, the code has to be updated.
* The user must exist on the target ThoughtSpot server.
* Passwords aren't currently supported, so as long as the user is known a valid token will be returned.
* All users current get FULL access.

## Contact
Primary author is [Bill Back](https://github.com/billdback-ts)