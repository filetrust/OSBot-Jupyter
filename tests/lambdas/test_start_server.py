import base64
from unittest                           import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

class test_run_command(Test_Helper):
    def setUp(self):
        super().setUp()
        self.aws_lambda = Lambda('osbot_jupyter.lambdas.start_server')
        self.result     = None
        self.png_data   = None
        #self.aws_lambda.add_module('osbot_browser')
        #self.aws_lambda.update_code()       # use when wanting to update lambda function

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    # def test_invoke_lambda(self):w
    #     #payload     = { 'repo_name': 'gs-notebook-gscs',  "channel": "GDL2EC3EE", "team_id": "T7F3AUXGV"}
    #     payload     = { 'repo_name': 'gs-notebook-risks', 'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV', 'user': 'U7ESE1XS7'}
    #     self.result = self.aws_lambda.invoke(payload)

    def test_invoke_lambda_bad_repo(self):
        payload     = { 'repo_name': 'gs-notebook-AAAAA', "team_id" : "T7F3AUXGV", "channel": "GDL2EC3EE"}
        self.result = self.aws_lambda.invoke(payload)


    def test_just_update(self):
        lambda_name = 'osbot_jupyter.lambdas.start_server'
        Deploy().deploy_lambda__jupyter(lambda_name)

    def test_invoke(self):
        lambda_name = 'osbot_jupyter.lambdas.start_server'
        Deploy().deploy_lambda__jupyter(lambda_name)
        payload = { 'repo_name'  : 'gwbot-jupyter-notebooks',
                    'channel'    : 'DRE51D4EM'              ,
                    'user'       : 'UR9UENEAW'              ,
                    'server_size': 'large'                  }
        result = Lambda(lambda_name).invoke(payload)
        self.result = result
