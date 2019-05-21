import config
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

    def get_instance_id_by_instance_ip(self, instance_ip):
        port = self.neutron.list_ports(
            fixed_ips=["ip_address={}".format(instance_ip)]
        )
        if port:
            import ipdb; ipdb.set_trace()

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

if __name__ == "__main__":
    ops = OpenstackClient()
    # print(ops.get_mac_address_from_ip('172.16.11.3'))
    # ops.find_compute_ip_by_instance_ip('172.16.11.3')
    print(ops.find_compute_ip_by_instance_ip('172.16.11.3'))


