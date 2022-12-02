# Team TALK 

Our group plans on creating a web application that will take user fitness data, either manually entered or entered through an existing fitness tracker’s API, and log it into a user account. Based on their input, we will create a leaderboard showing their username and their fitness score. Login authentication will hopefully use Google’s OAuth. The user will be able to record their information and see other users’ fitness goals and fitness history.

## Team Members and Roles

* [Tu Nguyen](https://nhutu1911.github.io/CIS350-HW2-NGUYEN/)
* [Logan Nommensen](https://github.com/muzak23/CIS350-HW2-Nommensen)
* [Kyle Smigelski](https://github.com/kylesmigelski/CIS350-HW2-Smigelski)
* [Andrew Slayton](https://github.com/Andrewslayton/CIS350-HW2-SLAYTON/blob/main/README.md)

## Prerequisites

## Run Instructions

[Visit the live website](https://talk.muzak23.com/)

To run locally:
* Clone the repository 
* Install requirements with `pip install -r requirements.txt`
* In the `/GVSU-CIS350-TeamTALK` directory, run `python3 -m venv venv` to create the virtual environment
* Activate the environment with `venv\Scripts\activate`
* Set the flask app: `$env:FLASK_APP = "talk"` (Powershell)
* Start the local server: `flask run`
* Connect to the local address on the browser of your choice!
