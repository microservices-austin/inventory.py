"""
Inventory Service
"""
import logging

from eventify.service import Service
from eventify.event import Event
from uuid import uuid4

from service.constants import commands
from service.handler import handle_transfer_inventory


logging.basicConfig(level=logging.DEBUG)

def event_handler(event, session=None): 
    event = Event(event)           # Transform event to object
    if event.name not in commands: # If the recieved event is not something
        return                     # we care about; do nothing.

    if event.name == 'TransferInventory':
        handle_transfer_inventory(event, session)


if __name__ == '__main__':
    consumer = Service(
        config_file='config.json', # Specify configuration
        callback=event_handler     # Define callback function
    ).start()                      # Start event loop
