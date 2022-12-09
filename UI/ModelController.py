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
    time.sleep(5)
