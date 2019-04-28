import json
import os
from time import sleep

from ipykernel.kernelbase import Kernel

from jupyter_client.kernelspec import KernelSpecManager
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from osbot_jupyter.api.Kernel_Install import Kernel_Install


class GSBot_Kernel_Install:
    def __init__(self):
        self.kernel_name     = 'GSBot'
        self.kernel_class    = GSBot_Kernel
        self.kernel_language = 'python'
        self.kernel_spec = {   "argv"        : ["python", "-m", self.kernel_class.__module__, "-f", "{connection_file}"],
                               "display_name": self.kernel_name    ,
                               "language"    : self.kernel_language,
                           }

class GSBot_Kernel(Kernel):

    implementation = 'GSBot'
    implementation_version = '0.1'
    banner = "GSBot (kernel)"



    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': '..gsbot response : ' + code}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        sleep(0.2)
        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
                }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=GSBot_Kernel)
