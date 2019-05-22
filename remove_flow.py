# Copyright SNSLab
# Author: Sa Pham Dang

import openstack
import utils


def remove_flow(flow_id, flow_name, attacker_ipv4_address,
                victim_ipv4_address, honeypot_ipv4_address):
    """Redirect Traffic from attacker to honeypot instance
    """


    ops = openstack.OpenstackClient()
    print("Generated Redirected OpenFlow Rules")
    # Locate switch to install
    print("Finding Switch")

    honeypot_fixed_ip = ops.get_fixed_ip_by_floating_ip(honeypot_ipv4_address)
    victim_fixed_ip = ops.get_fixed_ip_by_floating_ip(victim_ipv4_address)

    victim_compute_ip = ops.find_compute_ip_by_instance_ip(victim_fixed_ip)
    honeypot_compute_ip = ops.find_compute_ip_by_instance_ip(honeypot_fixed_ip)

    victim_switch_id = utils.find_switch_id_by_ip(victim_compute_ip)
    honeypot_switch_id = utils.find_switch_id_by_ip(honeypot_compute_ip)

    print("Victim Switch ID: {}".format(victim_switch_id))
    print("Honeypot Switch ID: {}".format(honeypot_switch_id))
    # Install flows
    utils.delete_flow(
        switch_id=victim_switch_id,
        table_id=27,
        flow_id=flow_id + "_forward_link"
    )
    utils.delete_flow(
        switch_id=honeypot_switch_id,
        table_id=28,
        flow_id=flow_id + "_reverse_link"
    )


if __name__ == "__main__":
    flow_id = 'demo_redirect_attack'
    flow_name = flow_id
    attacker_ipv4_address = '192.168.110.1'
    victim_ipv4_address = '192.168.110.171'
    honeyport_ipv4_address = '192.168.110.178'
    remove_flow(flow_id, flow_name, attacker_ipv4_address, victim_ipv4_address, honeyport_ipv4_address)
