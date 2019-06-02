import unittest
from unittest import TestCase

from osbot_aws.Globals import Globals
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jupyter.Deploy import Deploy


class test_Deploy_Lambda_Functions(TestCase):


    def test_deploy_lambda_functions(self):
        targets = [
                    'osbot_jupyter.lambdas.osbot'      ,   #   osbot.py    OSBot_Commands
                    'osbot_jupyter.lambdas.screenshot',
                    'osbot_jupyter.lambdas.start_server'
                   ]
        result = ""
        for target in targets:
            Deploy(target).deploy()
            result += " • {0}\n".format(target)

        text        = ":hotsprings: [osbot-gsuite] updated lambda functions"
        attachments = [{'text': result, 'color': 'good'}]
        slack_message(text, attachments)  # gs-bot-tests
        Dev.pprint(text, attachments)


if __name__ == '__main__':
    unittest.main()