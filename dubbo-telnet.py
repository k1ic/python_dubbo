#coding=utf-8
"""
Name: dubbo-telnet
Author: k1ic

Tested in python3.7
"""

import json
import telnetlib
import socket
import ast

class Dubbo(telnetlib.Telnet):

    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        super().__init__(host, port, timeout)
        self.write(b'\n')

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def invoke(self, service_name, method_name, arg):
        command_str = "invoke {0}.{1}({2})".format(
            service_name, method_name, json.dumps(arg))

        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        data = json.loads(data.decode(Dubbo.coding, errors='ignore').split('\n')[0].strip())
        return data

def load_data(file_path):
    res = []

    file = open(file_path, 'r')
    try:
        for line in file:
            line_dict = ast.literal_eval(line)
            #print(line_dict, type(line_dict))
            res.append(line_dict)
    finally:
        file.close()

    return res

if __name__ == '__main__':
    host = '172.16.34.127'
    port = 20880
    timeout = 0.1 #单位秒
    conn = Dubbo(host, port, timeout)

    service = 'com.yzb.service.clientapi.api.HotfixApi'
    method = 'getAlphaBeta'

    json_data = {
        "dataType":"peak"
    }

    # cat ./params.list
    #{"dataType":"peak"}
    #{"dataType":"peak"}
    #{"dataType":"peak"}
    args_list = load_data('./params.list')
    #print(args_list)

    for item in args_list:
        result = conn.invoke(
            service,
            method,
            item
        )

        print(item, result)

