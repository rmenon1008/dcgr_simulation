"""
Used to test client-specific functions in the ClientClientPayloadHandler.
"""
from mockito import mock

import mesa

from payload import ClientPayload
from peripherals.roaming_dtn_client_payload_handlers.cilent_payload_handler import ClientClientPayloadHandler

"""
Tests that payloads stored-to-be-sent can expire.
"""
def test_store_payload_refresh_payload_expires():
    # set up a dummy model object used by the ClientClientPayloadHandler object.
    schedule = mesa.time.RandomActivation(mesa.Model())
    dummy_model = mock({"schedule": schedule})

    # create the client_handler
    client_handler = ClientClientPayloadHandler("0", dummy_model)

    # create a payload object.
    payload = ClientPayload("0", "0", dummy_model.schedule.time)

    # store the payload object.
    client_handler.store_payload(payload)

    # assert that the payload object has been stored.
    assert payload in client_handler.payloads_to_send

    # move the schedule forward such that the payload expires.
    expire_timestamp = ClientPayload.EXPIRATION_LIFESPAN + 1
    for i in range(0, expire_timestamp):
        schedule.step()

    # refresh the client_handler.
    client_handler.refresh()

    # assert that the payload object is no longer present in the client_handler.
    assert payload not in client_handler.payloads_to_send


"""
Tests that records of payloads previously received can expire.
"""
def test_already_received_payload_ids_expiration():
    # set up a dummy model object used by the ClientClientPayloadHandler object.
    schedule = mesa.time.RandomActivation(mesa.Model())
    dummy_model = mock({"schedule": schedule})

    # create the client_handler
    client_handler = ClientClientPayloadHandler("0", dummy_model)

    # create the entry for the already_received_payload_ids list.
    already_received_entry = ("0", schedule.time)

    # store the entry in already_received_payload_ids
    client_handler.already_received_payload_ids.append(already_received_entry)

    # assert that the entry has been stored.
    assert already_received_entry in client_handler.already_received_payload_ids

    # move the schedule forward so the payload expires.
    schedule.step()

    # refresh the client_handler.
    client_handler.refresh()

    # assert that the entry is no longer present in the client_handler.
    assert already_received_entry not in client_handler.already_received_payload_ids