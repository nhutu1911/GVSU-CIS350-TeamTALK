Team name: TALK

Team members: Tu Nguyen, Logan Nommensen, Kyle Smigelski, Andrew Slayton

# Introduction

Our group plans on creating a web application that will take user fitness data, either manually entered or entered through an existing fitness tracker’s API, and log it into a user account. Based on their input, we will create a leaderboard showing their username and their fitness score. Login authentication will hopefully use Google’s OAuth. The user will be able to record their information and see other users’ fitness goals and fitness history.

On this website, users will be able to access daily challenges, which may be different exercises to help motivate them to keep active and add more fitness data and increase their score on the leaderboard. We believe the application will give users motivation with their fitness goals and it can become an inspiring community for everyone to accomplish goals they otherwise would potentially lack motivation for. These daily goals will also give users the ability to learn more about exercise if they are confused with what exercises to do, and they will learn about how the specific exercise on the daily challenge is beneficial to their health.

# Anticipated Technologies

Web server, database, fitness app API (ex. Strava, MyFitnessPal, iOS HealthKit), possible authentication API (ex. Login with Google OAuth), Flask

# Method/Approach

We would first create a skeleton website with a simple account system (no authentication) and basic raw data entry and storage. 
We will then start adding complexity to data entry, likely starting with formatted manual data entry then moving to the more complex external APIs if possible. 
We will then try to create a point-based system for competition, with challenges and incentives, followed by a leaderboard. Challenges and incentives will likely be added throughout the project.
We will try to have a more secure account system, likely using Google’s OAuth (Login with Google) if feasible.
After having all functions set up for the site, we will start working on the site layout and styling with CSS to make the page more user-friendly, then finish with testing.

# Estimated Timeline

Skeleton of the website with hopefully both basic account system and raw data entry by early October
Hook in external APIs for data entry or format manual data entry - By end of October
Create a point system with incentives and challenges - Throughout October through mid November
Create a point leaderboard - Alongside the point system, finishing soon after
More user-friendly layout with homepage - Early November
Authentication system for accounts - Early to mid November depending on Google OAuth feasibility
Front-end styling with CSS - Mid to late November
Testing - November

# Anticipated Problems

We anticipate difficulties incorporating/learning how to use a database to store and retrieve user data, as it is new to most of our group. We also may have trouble with user authentication/logging in as it will need to be secure, and may have trouble connecting to APIs requiring authentication as we will need to also find out how to authenticate with the APIs as an individual user.
