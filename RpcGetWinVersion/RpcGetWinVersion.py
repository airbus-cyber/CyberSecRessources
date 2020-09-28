#!/usr/bin/python

"""
Copyright 2020 by Nicolas Delhaye (@_Homeostasie_)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys, getopt
import struct

from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_WINNT, RPC_C_AUTHN_LEVEL_CONNECT, MSRPC_BIND
from impacket.dcerpc.v5.rpcrt import MSRPCHeader, MSRPCBind, MSRPCBindAck, SEC_TRAILER, CtxItem
from impacket.dcerpc.v5.dcomrt import IID_IObjectExporter
from impacket import ntlm
from impacket.uuid import uuidtup_to_bin



'''
bind_ntlm_authinfo
'''
def bind_ntlm_authinfo(dcerpc, iface_uuid): 
      
    # Build MSRPCBind information
    bind = MSRPCBind()
    item = CtxItem()
    item['AbstractSyntax'] = iface_uuid
    item['TransferSyntax'] = uuidtup_to_bin(('8a885d04-1ceb-11c9-9fe8-08002b104860', '2.0'))
    item['ContextID'] = 0
    item['TransItems'] = 1
    bind.addCtxItem(item)           
    
    # Build NTLM Authentication Negociate
    auth = ntlm.NTLMAuthNegotiate()
    auth['flags'] =  ntlm.NTLMSSP_NEGOTIATE_UNICODE
    
    # Build Security Trailer
    sec_trailer = SEC_TRAILER()
    sec_trailer['auth_type']   = RPC_C_AUTHN_WINNT
    sec_trailer['auth_level']  = RPC_C_AUTHN_LEVEL_CONNECT
    sec_trailer['auth_ctx_id'] = 0xb0b0d0ba
    
    # Build MSRPC Header
    packet = MSRPCHeader()
    packet['type'] = MSRPC_BIND
    packet['call_id'] = 1
    packet['flags'] = 0x03
    packet['pduData'] = str(bind)
    packet['sec_trailer'] = sec_trailer
    packet['auth_data'] = str(auth)   
    
    # Send MSRPC request
    dcerpc._transport.send(packet.get_packet())
    
    # Receive MSRPC response
    s = dcerpc._transport.recv()
    if s == 0:        
        print "Failed to retrieve a Bind response!"
        return 0
    
    resp = MSRPCHeader(s)
    return resp       

    
'''
display_os_version function
'''     
def display_os_version(data):
    bindResp = MSRPCBindAck(str(data))
    AuthData = ntlm.NTLMAuthChallenge(bindResp['auth_data'])
        
    version = AuthData['Version']
    major_ver = struct.unpack('B',version[0])[0]
    minor_ver = struct.unpack('B',version[1])[0]
    build_num = struct.unpack('H',version[2:4])[0] 
    
    print("Version %d.%d (Build %d)" % (major_ver,minor_ver,build_num))
    
        
'''
main function
'''          
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ht:",["target="])
    except getopt.GetoptError:
        print 'RpcGetWinVersion.py -t <target>'
        sys.exit(2)

    target_ip = "192.168.1.1"

    for opt, arg in opts:
        if opt == '-h':
            print 'RpcGetWinVersion.py -t <target>'
            sys.exit()
        elif opt in ("-t", "--target"):
            target_ip = arg

    stringBinding = r'ncacn_ip_tcp:%s' % target_ip    
    rpctransport = transport.DCERPCTransportFactory(stringBinding)    
    
    dcerpc = rpctransport.get_dce_rpc()      
    dcerpc.connect()      
    
    resp = bind_ntlm_authinfo(dcerpc, IID_IObjectExporter)
    display_os_version(resp)
     
        
if __name__ == "__main__":
   main(sys.argv[1:])

