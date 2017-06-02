import logging

from eventify.consumer import Consumer
from eventify.event import Event
from eventify.producer import Producer
from uuid import uuid4

from service.constants import commands, UPPER_CAPACITY, LOWER_CAPACITY
from service.db import connect_db, persist_event
from psycopg2 import sql

logging.basicConfig(level=logging.DEBUG)
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

    # Parse Message
    inventory_uuid = message.get('product_id')
    from_location = message.get('source_destination_id')
    to_location = message.get('to_destination_id')
    quantity_requested = message.get('quantity')

    try:
        if inventory_uuid is not None:
            # Do we have enough items in the source destination to
            # fulfill the inventory transfer request
            from_quantity = retrieve_current_quantity_per_location(inventory_uuid, from_location)
            if from_quantity < quantity_requested:
                raise ValueError('Unable to fulfill request due to insufficient quantity of product %s'.format(inventory_uuid))

            # Does the to source have capacity
            to_quantity = retrieve_current_quantity_per_location(inventory_uuid, to_location)
            if (to_quantity + quantity_requested) > UPPER_CAPACITY:
                raise ValueError('Target location does not have enough capacity to fulfill this request')

            # Write events to store
            new_from_quantity = from_quantity - quantity_requested
            new_to_quanitity = to_quantity + quantity_requested
            persist_event(new_from_quantity)
            persist_event(new_to_quantity)

            producer.emit_event(event_success)

    except ValueError as error:
        producer.emit_event(event_failed)
        



def retrieve_current_quantity_per_location(inventory_uuid, location):
    """
    Get the current quanity of a given inventory item
    in a given location id
    :param inventory_uuid: Inventory identifier
    :param location: Location identifier
    :return: Quantity per location
    """
    cursor = connect_db()
    cursor.execute(sql.SQL('''SELECT * FROM event_store
                              WHERE event_body->>'product_id' like %s'''), [inventory_uuid])
    events = cursor.fetchall()

    total_quantity = 0
    for event in events:
        quantity = event[2]['quantity']
        total_quantity += quantity
    return total_quantity
        

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
