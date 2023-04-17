"""
Contains the Epidemic class, which implements the epidemic algorithm w/ bundle expiration.
"""
from agent.client_agent import ClientAgent
from peripherals.routing_protocol.routing_protocol_common import Bundle, handle_payload


class Epidemic:

    def __init__(self, node_id, model, agent):
        self.node_id = node_id
        self.model = model
        self.agent = agent
        self.known_bundles = []
        self.num_bundle_sends = 0
        self.num_repeated_bundle_receives = 0
        self.num_bundle_reached_destination = 0

    """
    Receives + stores bundles of data for future propagation.
    """
    def handle_bundle(self, bundle: Bundle):
        if self.node_id == bundle.dest_id:
            handle_payload(self.model, self.node_id, bundle.payload)
            self.num_bundle_reached_destination += 1
        elif bundle not in self.known_bundles:
            self.known_bundles.append(bundle)
        else:
            self.num_repeated_bundle_receives += 1


    """
    Refreshes the state of the DTN object.  Called by the simulation at each timestamp.
    """
    def refresh(self):
        # remove any expired Bundles from the list of known_bundles which we wish to propagate.
        self.known_bundles = [bundle for bundle in self.known_bundles
                              if bundle.expiration_timestamp > self.model.schedule.time]

        # find all nearby agents, spam them with your Bundles.
        for neighbor_data in self.model.get_neighbors(self.agent):
            # obtain the agent associated with the neighbor
            neighbor_agent = self.model.agents[neighbor_data["id"]]

            # ignore exchanging data with ClientAgents or RouterAgents we're not connected to.
            if isinstance(neighbor_agent, ClientAgent) or not neighbor_data["connected"]:
                continue

            # if we've reached this point, the neighbor is a connected RouterAgent.
            #
            # send them all your Bundles.
            for bundle in self.known_bundles:
                neighbor_agent.routing_protocol.handle_bundle(bundle)
                self.num_bundle_sends += 1


    """
    Called by the agent and sent to the visualization for simulation history log.
    """
    def get_state(self):
        return {
            "num_repeated_bundle_receives": self.num_repeated_bundle_receives,
            "num_bundle_sends": self.num_bundle_sends,
            "num_bundle_reached_destination": self.num_bundle_reached_destination
        }


    """
    Private function used to send the passed Bundle to the specified node in the network.
    """
    def __send_bundle(self, bundle: Bundle, dest_id):
        dest_dtn_node = self.model.get_dtn_object(dest_id)
        dest_dtn_node.handle_bundle(bundle)