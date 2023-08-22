from app import db, Restaurants
all_ids = Restaurants.query.with_entities(Restaurants.venId).all()

for _ in all_ids:
    print(_[0])


    '''
    
    so am I able to just put my main daily crawler in here?

    
    
    '''