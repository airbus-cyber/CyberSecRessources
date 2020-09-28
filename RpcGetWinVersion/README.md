# RpcGetWinVersion

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

What is RpcGetWinVersion?
=========================

RpcGetWinVersion is a small tool that relies on Impacket to remotely grab the 
build number of a Windows OS over RPC. As no credentials are required, this 
makes it useful during reconnaissance stages.

This trick relies on sending a DCE/RPC Bind request with the Authentification
Information field set with the NTLMSSP_NEGOCIATE message type. Then, we need to 
leverage with the related DCE/RPC Bind_Ack response which holds a VERSION structure 
containing OS version information as part of the NTLMSSP_CHALLENGE message type.

Usage
=====

 * RpcGetWinVersion.py -t \<target\>
   
Examples
---------
Result from a Windows OS with Version 6.1 (Build 7601: Service Pack 1):
```bash
root@kali-2019:~/Desktop# ./RpcGetWinVersion.py -t 192.168.1.128 
Version 6.1 (Build 7601)
```

Result from a Windows OS with Version 2004 (OS Build 19401.450):
```bash
root@kali-2019:~/Desktop# ./RpcGetWinVersion.py -t 192.168.1.139
Version 10.0 (Build 19041)
```

Tested on
=========

 * Microsoft Windows Version 6.1 (Build 7601: Service Pack 1)
 * Microsoft Windows Version 1909 (OS Build 18363.1082)
 * Microsoft Windows Version 2004 (OS Build 19401.450)


Requirements
============
 * Python 2.7
 * Impacket

The Remote Procedure Call (RPC) port must be not filtered by the targeted machine.

License
=======

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Authors
=======
Nicolas Delhaye (@\_Homeostasie\_)
