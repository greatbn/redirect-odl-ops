
from .celery import dvnh_worker
from openstack import OpenstackClient
import generators
import utils
from mongodb import MongoDBWrapper


@dvnh_worker.task(bind=True, name='workers.handle.add_flow')
def add_flow_handler(self, data):
    print("Processing data: {}".format(data))

    victim_ipv4_address = data['victim_ip']
    attacker_ipv4_address = data['attacker_ip']
    id = 'handle_attack_{}_{}'.format(attacker_ipv4_address, victim_ipv4_address)
    ops = OpenstackClient()
    print("Get network id of victim Virtual Machine")
    victim_fixed_ip = ops.get_fixed_ip_by_floating_ip(victim_ipv4_address)

    victim_mac_address = ops.get_mac_address_from_ip(victim_fixed_ip)

    victim_net_id = ops.get_network_id_by_ip(victim_fixed_ip)
    print("Network ID: {}".format(victim_net_id))

    print("Creating Honeypot Instance on network {}".format(victim_net_id))
    server, honeypot_ipv4_address, honeypot_fixed_ip = ops.create_server(
        name=id,
        network_id=victim_net_id
    )


    print("Generating Redirect Flow Rules")

    fl_flow = generators.forward_link_ips_generate(
        flow_id=id,
        flow_name=id,
        honeypot_fixed_ip=honeypot_fixed_ip,
        attacker_ipv4_address=attacker_ipv4_address,
        victim_fixed_ip=victim_fixed_ip
    )

    rl_flow = generators.reverse_link_ips_generate(
        flow_id=id,
        flow_name=id,
        victim_ipv4_address=victim_ipv4_address,
        victim_mac_address=victim_mac_address,
        honeypot_ipv4_address=honeypot_ipv4_address,
        attacker_ipv4_address=attacker_ipv4_address
    )

    print("Finding Switch")
    
    victim_compute_ip = ops.find_compute_ip_by_instance_ip(victim_fixed_ip)
    honeypot_compute_ip = ops.get_compute_ip(server.__dict__['OS-EXT-SRV-ATTR:hypervisor_hostname'])

    victim_switch_id = utils.find_switch_id_by_ip(victim_compute_ip)
    honeypot_switch_id = utils.find_switch_id_by_ip(honeypot_compute_ip)

    print("Victim Switch ID: {}".format(victim_switch_id))
    print("Honeypot Switch ID: {}".format(honeypot_switch_id))
    # Install flows
    print("Installing Forward Link on {}".format(victim_compute_ip))
    utils.add_flow(
        switch_id=victim_switch_id,
        flow_data=fl_flow,
        table_id=27,
        flow_id=id + "_forward_link"
    )
    print("Install Reverse Link on {}".format(honeypot_compute_ip))
    utils.add_flow(
        switch_id=honeypot_switch_id,
        flow_data=rl_flow,
        table_id=28,
        flow_id=id + "_reverse_link"
    )


    print("Traffic from attacker {} to victim {} is redirected to {} now".format(
        attacker_ipv4_address,
        victim_ipv4_address,
        honeypot_ipv4_address
    ))

    db = MongoDBWrapper()
    col = {
        'flow_id': id,
        'attacker_ip': attacker_ipv4_address,
        'victim_ip': victim_ipv4_address,
        'honeypot_ip': honeypot_ipv4_address,
        'honeypot_instance_id': server.id,
        'victim_switch_id': victim_switch_id,
        'honeypot_switch_id': honeypot_switch_id,
        'honeypot_fixed_ip': honeypot_fixed_ip
    }
    db.update_flow(
        data,
        col
    )
    print("Stored in databases")


@dvnh_worker.task(bind=True, name='workers.handle.del_flow')
def del_flow_handler(self, data):
    victim_switch_id = data['victim_switch_id']
    honeypot_switch_id = data['honeypot_switch_id']

    flow_id = data['flow_id']

    print("Deleting Flow in victim switch {}".format(victim_switch_id))
    utils.delete_flow(
        switch_id=victim_switch_id,
        table_id=27,
        flow_id=flow_id + "_forward_link"
    )
    print("Deleting Flow in honeypot switch {}".format(honeypot_switch_id))
    utils.delete_flow(
        switch_id=honeypot_switch_id,
        table_id=28,
        flow_id=flow_id + "_reverse_link"
    )
    print("Deleted Redirect Flow Traffic for attacker {}. Victim {}".format(
        data['attacker_ip'],
        data['victim_ip']
    ))

    ops = OpenstackClient()
    db = MongoDBWrapper()

    print("Deleting Honeypot instance")

    fip = ops.get_floatingip(data['honeypot_fixed_ip'])
    try:
        ops.delete_floatingip(fip['floatingips'][0]['id'])
    except IndexError:
        print("Floating IPs is deleted")
    ops.delete_server(data['honeypot_instance_id'])
    
    # server = ops.create_server('test', network_id, is_floating=False, image_id='db9bc435-d88e-4b17-b27d-747fbdced9d8')
    # ops.delete_server(server.id)
    

    db.delete_flow(
        {
            'attacker_ip': data['attacker_ip'],
            'victim_ip': data['victim_ip']
        }
    )
    print("Deleted in database")
    
    
