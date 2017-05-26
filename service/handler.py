import logging

from eventify.consumer import Consumer
from eventify.event import Event
from eventify.producer import Producer
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
#connection_string = 'postgres://dev:test1234@localhost:5432/inventory';


def handle_transfer_inventory(message, producer):
    """
    Handle Transfer Inventory
    TODO: Check capcity - capcity = 100
    """

    # Setup Events
    event_start = Event('InventoryTransferInitiated', message)
    event_success = Event('InventoryTransferred', message)
    event_failed = Event('InventoryTransferFailed', message)

    # Publish Events
    producer.emit_event(event_start)
    if True:
        producer.emit_event(event_success)
    else:
        producer.emit_event(event_failed)

def handleAdjustInventory(message):
    pass

def handlePickInventory(message):
    pass

def persistEvent(event_name, message):
    pass


def handler(**kwargs): 
    event_name = kwargs.keys()[0]
    if event_name not in commands:
        return

    event_body = kwargs[event_name]
    producer = Producer(config_file='config.json')
    if event_name == 'TransferInventory':
        handle_transfer_inventory(event_body, producer)

if __name__ == '__main__':
    consumer = Consumer(
        config_file='config.json', # Specify configuration
        callback=handler           # Define callback function
    )
    consumer.start()               # Start the event loop
