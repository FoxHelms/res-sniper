# Purpose

ResSniper is a web app that allows you to book reservations at restaurants that are otherwise impossible to get. 

This app is best used for restaurants that have very limited reservation openings, which are taken within minutes (or even seconds), of being posted.
Note: this app is NOT suited for automatically making reservations at regular restaurants, as it does not offer much control over reservation time, party size, etc. 

# How to use it
The app will ask you to login with your resy credentials. This information is cached on your machine and sent directly to Resy, it is never stored anywhere remotely.

Once logged in, you can paste a link to a *resy.com* restaurant page. The app will add this restaurant to your list. To remove it from the list, just click the minus button. 

That's all you have to do! Every day at 9am (when new reservation times are released), the app will automatically look for available times and try to book them. 

If the app succeeds, you will get a confirmation email from Resy that has the details of your reservation. 

Enjoy!

## How it works: Abstract View

This app is a "hail mary" for booking a reservation. It's meant to work quickly, so it trades some basic control for speed. 

This has lead to the following design decisions, which I think are worth noting. 

### Links as User Input

An older version of the app allowed you to type in a restaurant name, which is more familiar to a user than inputing a link. 
However, it was hard to prevent users from submitting something that was not a restaurant name. 
If the restaurant was part of a franchise, it was nearly impossible to specify what branch you wanted to reserve. 
For technical reasons that are not interesting, it was hard to search for restaurants outside the city of the computer you were using. 
By pasting a link, it became convenient to specify a branch and choose a restaurant anywhere in the world. 


### Lightweight User Profile Technique

In earlier versions of this app, login data was stored locally so that the bot could create reservations on the user's behalf. 
This is obviously insecure, but the bot does need a way to authenticate each reservation, otherwise resy has no idea who is doing what. 
The solution is to store the authentication token locally, as it is meaningless outside a resy session context and does not provide any user data, nor can user data be extracted. 
This technique offers the functionality of a user account without needing a database or encryption algorithm. 
This decision was essential in reducing the app's complexity and therefore greatly increased speed. 


### Reducing Post Requests

Resy servers deal with a lot of bots. Many times while developing this app, resy start returning errors for all of my post requests, which it thought were bot-originated.
My solution to this was to minimize the number of post requests the bot performs so that by the time the servers catch on, the bot already finished its work :sunglasses:
Usually, a post request is required to authenticate a user and to book a reservation. 
By performing the post request when the user provides their login data (one time), and preserving that token for my reservation requests, I no longer need to authenticate the user when I make a reservation, cutting my post requests down to just one per reservation. 


### Prioritizing Restaurant with Fewest Available Slots

There is no way to prioritize the list of restaurants in the app. 
Instead, what happens is the number of available slots at each restaurant is counted, and the restaurant with the fewest open slots is prioritized. 
This gives you the highest chance of booking a reservation.



## This Project Demonstrates


### Resy API Interraction

Resy does not have a publically available API. 
I had to reverse engineer the API myself by studying my network traffic as I interracted with the website. 
From here, I was able to use the Python requests module to interract with the website. 
As an interesting example: you can only view open slots at a restaurant if you include the restaurant name as json in your post request. Using any other method or datatype will not return open slots. 


### Unit Testing and Mocking (pytest)

As mentioned above, resy would often shut down my bot behavior. I used unittest to mock the resy API behavior so that I could test my functions without relying on Resy servers. 


### Advanced Flask framework usage

I utilized funtionality such as client-side caching, interractive forms, and conditional redirects, and testing clients/servers. 


### YML Workflows

I utilized GitActions for CL/CI to automatically test my code on each pull request. 


### Advanced Python Requests Module Usage

I wrote a wrapper for the requests module that handles errors, controls methods and query datatypes, and reduces clutter in the codebase. 
I also wrote unit tests that mock server functionality. 
I converted cURL commands to python requests. 

### Containerization with Docker

I built a DockerImage so that this app could be easily deployed to servers and other local machines. 

### To Do
- [] Host app on PythonAnywhere (paid tier)
