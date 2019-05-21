# Copyright SNSLab
# Author: Sa Pham Dang

import generators
import openstack
import utils



def redirect_attack(flow_id, flow_name, attacker_ipv4_address,
                    victim_ipv4_address, honeypot_ipv4_address):
    """Redirect Traffic from attacker to honeypot instance
    """
    # Get Mac Address
    print("Get Mac Address")
    ops = openstack.OpenstackClient()
    honeypot_mac_address = ops.get_mac_address_from_ip(honeypot_ipv4_address)
    victim_mac_address = ops.get_mac_address_from_ip(victim_ipv4_address)
    print("MAC Address Honeypot: {}".format(honeypot_mac_address))
    print("MAC Address Victim: {}".format(victim_mac_address))
    # Generate flow 

    fl_flow = generators.forward_link_generate(
        flow_id=flow_id,
        flow_name=flow_name,
        honeypot_ipv4_address=honeypot_ipv4_address,
        honeypot_mac_address=honeypot_mac_address,
        attacker_ipv4_address=attacker_ipv4_address,
        victim_ipv4_address=victim_ipv4_address
    )

    rl_flow = generators.reverse_link_generate(
        flow_id=flow_id,
        flow_name=flow_name,
        victim_ipv4_address=victim_ipv4_address,
        victim_mac_address=victim_mac_address,
        honeypot_ipv4_address=honeypot_ipv4_address,
        attacker_ipv4_address=attacker_ipv4_address
    )

    print("Generated Redirected OpenFlow Rules")
    # Locate switch to install
    print("Finding Switch")
    victim_compute_ip = ops.find_compute_ip_by_instance_ip(victim_ipv4_address)
    honeypot_compute_ip = ops.find_compute_ip_by_instance_ip(honeypot_ipv4_address)
    victim_switch_id = utils.find_switch_id_by_ip(victim_compute_ip)
    honeypot_switch_id = utils.find_switch_id_by_ip(honeypot_compute_ip)
    print("Victim Switch ID: {}".format(victim_switch_id))
    print("Honeypot Switch ID: {}".format(honeypot_switch_id))
    # Install flows
    utils.add_flow(
        switch_id=victim_switch_id,
        flow_data=fl_flow,
        table_id=51,
        flow_id=flow_id + "_forward_link"
    )
    utils.add_flow(
        switch_id=honeypot_switch_id,
        flow_data=rl_flow,
        table_id=51,
        flow_id=flow_id + "_reverse_link"
    )



if __name__ == "__main__":
    flow_id = 'demo_redirect_attack'
    flow_name = flow_id
    attacker_ipv4_address = '172.16.11.5'
    victim_ipv4_address = '172.16.11.3'
    honeyport_ipv4_address = '172.16.11.4'
    redirect_attack(flow_id, flow_name, attacker_ipv4_address, victim_ipv4_address, honeyport_ipv4_address)
