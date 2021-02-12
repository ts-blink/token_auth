# Get Token Service

This project is a simple Flask server that will act as a trusted authentication server.

**_WARNING:  Do not share this code outside of ThoughtSpot!  It contains login info to a dev server._**

Calls to the server are in the form of `https://<URL>:5000/gettoken/<username>`

## Python Dependencies
* Python 3 (virtual environment recommended)
* flask
* flask_cors
* requests

## Deploy and Configure

This service should be deployed to an environment that is
1. Accessible to the embedding service that will need to use token authentication
2. Have access to the ThoughtSpot cluster APIs (usually via HTTPS)

Steps to deploy and run:
1. Create a folder on the server that will host the gettoken service.
2. Create a virtual environment using `python3 -m venv ./venv`.  While this step isn't technically required, it is recommended to avoid conflicts in package dependencies.
3. Deploy the `gettoken.py`, `gettoken.config`, `start_flask.sh` scripts to the new folder.
4. Modify the `gettoken.config` file to have the proper settings for your ThoughtSpot cluster.
5. Modify `start_flask.sh` to point to have the correct folder information.

You should now be able to run `bash start_flask.sh` to start the server.  The server listens on port 5000.  

## Notes

If the server or login change, the code has to be updated.
* The user must exist on the target ThoughtSpot server, or you will get an error.
* Passwords aren't currently supported, so as long as the user is known a valid token will be returned.
* All users current get FULL access.

## Contact
Primary author is [Bill Back](https://github.com/billdback-ts)