# test_export_config.py
import sys 
from ncclient import manager 
from ncclient import operations 

#Fill the device information and establish a NETCONF session
def huawei_connect():
    return manager.connect(host="192.168.150.201",
                            port=830,
                            username="netconf",
                            password="Admin@1234",
                            hostkey_verify = False,
                            device_params={'name': "huaweiyang"},
                            allow_agent = False,
                            look_for_keys = False)

def test_connect(): 
    with huawei_connect() as m: 
 
        n = m._session.id         
        print("The session id is %s." % (n)) 
 
if __name__ == '__main__':
    test_connect()