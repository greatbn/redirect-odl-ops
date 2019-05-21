import config
import requests
from requests.auth import HTTPBasicAuth


auth = HTTPBasicAuth(username=config.ODL_USERNAME, password=config.ODL_PASSWORD)


def find_switch_id_by_ip(switch_ip):

    url = '{}/restconf/operational/opendaylight-inventory:nodes'.format(
        config.API_URL)
    r = requests.get(url, auth=auth)
    if r.status_code == 200:
        nodes = r.json()['nodes']['node']
        for node in nodes:
            if node['flow-node-inventory:ip-address'] == switch_ip:
                return node['id']
    else:
        print("Something went wrong!!")


def _build_flow_url(switch_id, table_id, flow_id):
    url = "{api_url}/restconf/config/opendaylight-inventory:nodes/node/{switch_id}/flow-node-inventory:table/{table_id}/flow/{flow_id}".format(
        api_url=config.API_URL,
        switch_id=switch_id,
        table_id=table_id,
        flow_id=flow_id
    )
    return url


def add_flow(switch_id, flow_data, table_id, flow_id):
    """Add a new flow to Opendaylight
    """

    url = _build_flow_url(switch_id, table_id, flow_id)
    headers = {
        'Content-Type': 'application/xml'
    }
    r = requests.put(url, data=flow_data, headers=headers, auth=auth)
    if r.status_code == 201:
        return True
    else:
        print("Something went wrong!!!")
        print(r.content)
        print(r.status_code)
        return False


def delete_flow(switch_id, table_id, flow_id):

    url = _build_flow_url(switch_id, table_id, flow_id)

    r = requests.delete(url, auth=auth)
    if r.status_code == 200:
        return True
    else:
        print("Something went wrong!!!!")
        return False


if __name__ == "__main__":
    print(find_switch_id_by_ip('10.4.0.112'))