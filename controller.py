from typing import List

'''
This should be able to take user input and add it to the list that the resbot checks
'''

def get_rest_from_user(usrStr: str) -> str:
    '''ask user for restaurant name and convert to url string'''
    return usrStr.replace(' ','-').lower()

'''

Actually, I'm gonna make it write to a db. 



Since the interface here is a web app i'm going to go ahead and start that. Yeah, that makes sense. 


'''