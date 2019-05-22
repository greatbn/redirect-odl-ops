import config
import time
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from neutronclient.v2_0 import client as neutron_client
from novaclient.client import Client as nova_client



class OpenstackClient(object):
    def __init__(self):
        self.sess = self.create_admin_session()
        self.neutron = neutron_client.Client(session=self.sess)
        self.nova = nova_client('2', session=self.sess)


    def create_admin_session(self):
        keystone_authtoken = {
            'auth_url': config.OS_AUTH_URL,
            'username': config.OS_USERNAME,
            'password': config.OS_PASSWORD,
            'project_name': config.OS_PROJECT_NAME,
            'user_domain_name': config.OS_USER_DOMAIN_NAME,
            'project_domain_name': config.OS_PROJECT_DOMAIN_NAME
        }
        auth = v3.Password(**keystone_authtoken)
        return Session(auth=auth)

    def get_mac_address_from_ip(self, ip_address):
        port = self.neutron.list_ports(
            fixed_ips=["ip_address={}".format(ip_address)]
        )
        if port:
            return port["ports"][0]["mac_address"]

    # def get_instance_id_by_instance_ip(self, instance_ip):
    #     port = self.neutron.list_ports(
    #         fixed_ips=["ip_address={}".format(instance_ip)]
    #     )
    #     if port:
    #         import ipdb; ipdb.set_trace()

    def get_port_by_ip(self, ip):
        port = self.neutron.list_ports(
            fixed_ips=["ip_address={}".format(ip)]
        )
        return port

    def find_compute_ip_by_instance_ip(self, instance_ip):
        port = self.neutron.list_ports(
            fixed_ips=["ip_address={}".format(instance_ip)]
        )
        if port:
            compute_node = port['ports'][0]['binding:host_id']
            print("Instance {} is on node: {}".format(instance_ip, compute_node))
            hypervisors = self.nova.hypervisors.list()
            for h in hypervisors:
                if h.hypervisor_hostname == compute_node:
                    return h.host_ip



    def get_compute_ip(self, compute_name):
        hypervisors = self.nova.hypervisors.list()
        for h in hypervisors:
            if h.hypervisor_hostname == compute_name:
                return h.host_ip


    def get_fixed_ip_by_floating_ip(self, floating_ip):
        for fip in self.neutron.list_floatingips()['floatingips']:
            if fip['floating_ip_address'] == floating_ip:
                return fip['fixed_ip_address']

    def create_server(self, name, network_id):

        flavor_id = config.HONEYPOT_INSTANCE_FLAVOR_ID
        image_id = config.HONEYPOT_IMAGE_ID
        key_name = config.HONEYPOT_KEYPAIR_NAME

        networks = [
            {
                'net-id': network_id
            }
        ]
        s = self.nova.servers.create(
            name=name,
            image=image_id,
            flavor=flavor_id,
            key_name=key_name,
            nics=networks
        )
        server = self.nova.servers.get(s.id)
        while server.status not in ['ACTIVE', 'ERROR']:
            server = self.nova.servers.get(server.id)
            time.sleep(2)
        if server.status == 'ERROR':
            print("Cannot create server")
            return False
        fixed_ip = server.addresses[s.addresses.keys()[0]][0]['addr']
        port = self.get_port_by_ip(fixed_ip)
        fip = self.create_floatingip()
        self.associate_floatingip(fip['floatingip']['id'], port['ports'][0]['id'])
        
        floating_ip_address = fip['floatingip']['floating_ip_address']
        return server, floating_ip_address, fixed_ip

    def get_network_id_by_ip(self, instance_ip):
        port = self.neutron.list_ports(
            fixed_ips=["ip_address={}".format(instance_ip)]
        )
        if port:
            return port['ports'][0]['network_id']

    def create_floatingip(self):
        fip = self.neutron.create_floatingip(
            {
            'floatingip': 
                {
                'floating_network_id': config.EXTERNAL_NETWORK_ID
                }
            }
        )
        return fip

    def associate_floatingip(self, floatingip, port_id):

        try:
            self.neutron.update_floatingip(
                floatingip,
                {
                    'floatingip': {
                        'port_id': port_id
                    }
                }
            )
            return True
        except Exception as e:
            return False
        
if __name__ == "__main__":
    ops = OpenstackClient()
    # print(ops.get_network_id_by_ip('172.16.11.5'))
    # ops.find_compute_ip_by_instance_ip('172.16.11.3')
    # print(ops.find_compute_ip_by_instance_ip('172.16.11.3'))
    # print(ops.get_fixed_ip_by_floating_ip('192.168.110.178'))
    net = ops.get_network_id_by_ip('172.16.11.5')
    print("Found network id" , net)
    server, fip, fixed_ip = ops.create_server('sapd-test-4', net)
    print(server.__dict__)
    print(fip)
    print(fixed_ip)
    # fip = ops.create_floatingip()
    


    



