# To Do - Prioritized

- [ ] Write new tests for all classes, and test more cases of same functions (not just one and done), Mock bot tests for when resy misbehaves.
-- [X] Requester
-- [X] Authenticator
-- [ ] Rest Identifier
-- [ ] Time Checker
-- [ ] Booker
-- [ ] Web App
-- [ ] Conv_string
-- [ ] Find Venue


## Everything Else

- [ ] Document the abstractions. Why classes and files split the way I did? Does my flowchart make sense?
- [ ] Change website so that you just paste link to the resy page of restaurant. Adds to list as hyperlinked rest name. 
- [ ] Write Fxx?
- [ ] Remove secret key from repo! Ignore it. 
- [ ] Expand This project demonstrates: more detail about reverse engineering: what did you discover and use?
- [ ] Rename cryptic
- [ ] Polish pass on all doc strings, should make it so that person doesn't have to read code. 
- [ ] remove file for conv_string. Just add to code or smthng
- [ ] Encrypted =/= decrypted and decrypted(encrypted(input)) = input
- [ ] Record quick video using the software so that someone can see the app in action if they dont wanna build it. 


- [ ] Run Docker in project folder
- [ ] host everything on Heroku
- [ ] Use Cron To Go to run MakeRes on db every morning at 9am EST. 

### Done


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