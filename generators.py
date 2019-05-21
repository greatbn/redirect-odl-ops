from jinja2 import Environment, FileSystemLoader
from constants import *

def create_env():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    return env


def forward_link_generate(flow_id, flow_name, honeypot_ipv4_address,
                          honeypot_mac_address, attacker_ipv4_address,
                          victim_ipv4_address):
    env = create_env()

    template = env.get_template(FORWARD_LINK_TEMPLATE_FILE)
    flow = template.render(flow_id=flow_id,
                           flow_name=flow_name,
                           honeypot_ipv4_address=honeypot_ipv4_address,
                           honeypot_mac_address=honeypot_mac_address,
                           attacker_ipv4_address=attacker_ipv4_address,
                           victim_ipv4_address=victim_ipv4_address)

    return flow


def reverse_link_generate(flow_id, flow_name, victim_ipv4_address,
                          victim_mac_address, honeypot_ipv4_address,
                          attacker_ipv4_address):
    env = create_env()

    template = env.get_template(REVERSE_LINK_TEMPLATE_FILE)
    flow = template.render(flow_id=flow_id,
                           flow_name=flow_name,
                           victim_ipv4_address=victim_ipv4_address,
                           victim_mac_address=victim_mac_address,
                           honeypot_ipv4_address=honeypot_ipv4_address,
                           attacker_ipv4_address=attacker_ipv4_address)

    return flow


def forward_link_ips_generate(flow_id, flow_name, honeypot_fixed_ip,
                              attacker_ipv4_address,
                              victim_fixed_ip):
    env = create_env()

    template = env.get_template(FORWARD_LINK_FIPS_TEMPLATE_FILE)
    flow = template.render(flow_id=flow_id,
                           flow_name=flow_name,
                           honeypot_fixed_ip=honeypot_fixed_ip,
                           attacker_ipv4_address=attacker_ipv4_address,
                           victim_fixed_ip=victim_fixed_ip)

    return flow


def reverse_link_ips_generate(flow_id, flow_name, victim_ipv4_address,
                              victim_mac_address, honeypot_ipv4_address,
                              attacker_ipv4_address):
    env = create_env()
    template = env.get_template(REVERSE_LINK_FIPS_TEMPLATE_FILE)
    flow = template.render(flow_id=flow_id,
                           flow_name=flow_name,
                           victim_ipv4_address=victim_ipv4_address,
                           victim_mac_address=victim_mac_address,
                           honeypot_ipv4_address=honeypot_ipv4_address,
                           attacker_ipv4_address=attacker_ipv4_address)

    return flow


if __name__ == "__main__":
    flow_id = 'test_redirect_fl'
    flow_name = flow_id
    honeypot_ipv4_address = '172.16.11.4'
    honeypot_mac_address = 'fa:16:3e:61:d0:1d'
    attacker_ipv4_address = '192.168.110.14'
    victim_ipv4_address = '172.16.11.3'
    print("Generate Forward link flow")
    print(forward_link_generate(flow_id, flow_name, honeypot_ipv4_address,
                                honeypot_mac_address, attacker_ipv4_address,
                                victim_ipv4_address))
