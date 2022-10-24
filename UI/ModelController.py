'''
Contains functionality and 
abstraction of function calls 
to feed recent topics from the database
into the topic modeler
'''
import time

# Global Value for event callback
class Globals(object):
    PROGRESS = 0

# Main routine to begin maintence on topic modeler
def model_main():
    # Input model code here
    x = 0
    Globals.PROGRESS = x
    while Globals.PROGRESS < 100:
        Globals.PROGRESS += 1
        time.sleep(3)

