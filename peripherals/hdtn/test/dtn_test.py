import sys
from mockito import spy, verify

import pytest

from peripherals.hdtn.dtn import Dtn
from peripherals.hdtn.hdtn_bundle import Bundle

"""
Method used to setup DTN objects for this file's unit tests.
"""
@pytest.fixture()
def setup():
    # setup the 5 nodes (0, 1, 2, 3, 4).
    # we set them up wrapped in a "spy" so we can easily peek into method call stats.
    dtn_dict = {}
    dtn_dict[0] = spy(Dtn(0, dtn_dict))
    dtn_dict[1] = spy(Dtn(1, dtn_dict))
    dtn_dict[2] = spy(Dtn(2, dtn_dict))
    dtn_dict[3] = spy(Dtn(3, dtn_dict))
    dtn_dict[4] = spy(Dtn(4, dtn_dict))

    # link-up the nodes as follows with the respective timestamps...
    # 0 -> 1:  @3-5
    # 0 -> 2:  @0->inf
    # 2 -> 1:  @0->inf
    # 0 -> 3:  @0->inf
    for node in dtn_dict.values():
        node.add_link(0, 1, 3, sys.maxsize, 100)
        node.add_link(0, 2, 0, sys.maxsize, 100)
        node.add_link(2, 1, 0, sys.maxsize, 100)
        node.add_link(0, 3, 0, sys.maxsize, 100)

    yield dtn_dict

"""
Tests sending a Bundle when the best route is indirect.

(@timestamp = 0, the best route is 0->2->1)
"""
def test_handle_bundle_best_route_indirect(setup):
    dtn_dict = setup

    # create the Bundle to send.
    bundle = Bundle(0, 1)

    # have node 0 handle the Bundle.
    dtn_dict[0].handle_bundle(bundle)

    # assert that the bundle was sent to node 2 and node 1.
    verify(dtn_dict[0], times=1).handle_bundle(...)
    verify(dtn_dict[2], times=1).handle_bundle(...)
    verify(dtn_dict[1], times=1).handle_bundle(...)

"""
Tests sending a Bundle when the best route is indirect.

(@timestamp = 0, the best route is 0->2->1)
"""
def test_handle_bundle_best_route_indirect(setup):
    dtn_dict = setup

    # create the Bundle to send.
    bundle = Bundle(0, 1)

    # move all Dtn objects forward to timestamp=3
    for dtn in dtn_dict.values():
        dtn.refresh()
        dtn.refresh()
        dtn.refresh()

    # have node 0 handle the Bundle.
    dtn_dict[0].handle_bundle(bundle)

    # assert that the bundle was only sent to node 1.
    verify(dtn_dict[0], times=1).handle_bundle(...)
    verify(dtn_dict[1], times=1).handle_bundle(...)
    verify(dtn_dict[2], times=0).handle_bundle(...)

"""
Tests sending a Bundle when the best route is indirect.

(@timestamp = 0, the best route is 0->2->1)
"""
def test_handle_bundle_stores_bundle_sends_once_linked(setup):
    dtn_dict = setup

    # create the Bundle to send.
    bundle = Bundle(0, 4)

    # have node 0 handle the Bundle.
    dtn_dict[0].handle_bundle(bundle)

    # assert that the bundle was not sent to node 4.
    verify(dtn_dict[0], times=1).handle_bundle(...)
    verify(dtn_dict[4], times=0).handle_bundle(...)

    # link-up node 3 and node 4 in node 0 and node 3's contact plans.
    dtn_dict[0].add_link(
        source=3,
        dest=4,
        start_time=0,
        end_time=sys.maxsize,
        rate=100
    )
    dtn_dict[3].add_link(
        source=3,
        dest=4,
        start_time=0,
        end_time=sys.maxsize,
        rate=100
    )

    # assert that the linkings caused 4 to receive the bundle.
    verify(dtn_dict[3], times=1).handle_bundle(...)
    verify(dtn_dict[4], times=1).handle_bundle(...)