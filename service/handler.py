import json
import logging

from uuid import uuid4

from eventify.event import Event
from psycopg2 import sql

from service.constants import UPPER_CAPACITY
from service.db import connect_db

logging.basicConfig(level=logging.DEBUG)


def handle_transfer_inventory(event, producer):
    """
    Handle Transfer Inventory
    TODO: Check capcity - capcity = 100
    """
    # Setup Events
    event_start = Event({"name": "InventoryTransferInitiated", "message": event.message})
    event_success = Event({"name": "InventoryTransferred", "message": event.message})
    event_failed = Event({"name": "InventoryTransferFailed", "message": event.message})

    # Publish Events
    producer.emit_event(event_start)

    # Parse Message
    message = json.loads(event.message)
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
            new_to_quantity = to_quantity + quantity_requested
            producer.emit_event(Event({
                "name": "InventoryTotal",
                "message": {
                    "from_quanity": new_from_quantity,
                    "to_quanity": new_to_quantity,
                    "inventory_uuid": inventory_uuid
                }
            }))
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
