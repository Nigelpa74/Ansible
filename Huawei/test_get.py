# test_export_config.py
import sys
import logging 
from ncclient import manager
from ncclient import operations

log = logging.getLogger(__name__)

FILTER = '''<ifm xmlns="urn:huawei:yang:huawei-ifm">
                <interfaces>
                    <interface>
                        <name/>
                        <mtu/>
                    </interface>
                </interfaces>
            </ifm>'''

# Fill the device information and establish a NETCONF session
def huawei_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify = False,
                           device_params={'name': "huaweiyang"},
                           allow_agent = False,
                           look_for_keys = False)

def test_get(host, port, user, password):
    #1.Create a NETCONF session
    with huawei_connect(host, port=port, user=user, password=password) as m:
        n = m._session.id
        print("The session id is %s." % (n))

        #2.Send get RPC and print RPC reply
        get_reply = m.get([FILTER])
        print(get_reply)

if __name__ == '__main__':
    test_get(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])