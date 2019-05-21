from marshmallow import ValidationError
import ipaddress


def validate_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        raise ValidationError('IP Address {} is not right format'.format(ip))

