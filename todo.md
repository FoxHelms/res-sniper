# To Do - Prioritized

- [ ] Run Docker in project folder
-- [ ] Add to readme



## Everything Else

- [ ] Record quick video using the software so that someone can see the app in action if they dont wanna build it. 
- [ ] host everything on Heroku
- [ ] Use Cron To Go to run MakeRes on db every morning at 9am EST. 

### Done



- [X] Document the abstractions. Why classes and files split the way I did? Does my flowchart make sense?
-- [X] Web app takes links instead of searches, for eease of experience
-- [X] Resy misbehaved a lot with my post requests, so separating classes by type of get/post behavior
-- [X] Prioritize rest with shorter slot lists because less chances of getting res.
-- [X] No encryption, just write auth token to server so i dont need to save login info
- [X] Expand "This project demonstrates": more detail about reverse engineering: what did you discover and use?
-- [X] Using network inspector to find api links, copying cURL, converting to python request
- [X] INSTEAD of importing rc, just import login data and do decryption in sniper. 
- [X] Change book token method from get to post json
- [X] Polish pass on all doc strings, should make it so that person doesn't have to read code. 
- [X] Remove secret key from repo! Ignore it. 
- [X] Rename cryptic
- [X] Change website so that you just paste link to the resy page of restaurant. Adds to list as hyperlinked rest name. 
- [X] remove file for conv_string. Just add to code or smthng
- [X] Write new tests for all classes, and test more cases of same functions (not just one and done), Mock bot tests for when resy misbehaves.
-- [X] Requester
-- [X] Add something to requester that raises an exception if not json data is returned???
-- [X] Authenticator
-- [X] Rest Identifier
-- [X] Time Checker
-- [X] Booker
-- [X] Web App
-- [X] Conv_string (renamed)
-- [X] Find Venue
- [X] How to find all available slots at a restaurant without posting a date?
- [X] Split resbot class into: auth, time chk, booker, dater, poster/getter?
- [X] How to rework the api? What makes most sense from a user perspective?
- [X] send to Nick for feedback
- [X] Clean up code! Documentation, annotation, etc.
- [X] Improve tests. 
- [X] Error pages
- [X] Add en/decryption to resbot, resy config, app.py
- [X] Update main reservation folder so that it only tries one time on list (first index or first index at 8pm)
- [X] Write daily function that iterates through database and makes reservations. 
- [X] Add feature to increment day whenever there's a successful reservation. 
- [X] learn how to add proxies to requests
- [X] write css for home page