from time                                import sleep
from unittest                            import TestCase
from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper


class test_OSBot_Jupyter_Create_Code_Build(Test_Helper):

    def setUp(self):
        super().setUp()
        #Deploy().setup()
        self.project_name = 'OSBot-Jupyter'
        self.iam             = IAM()
        self.account_id      = self.iam.account_id()
        self.region          = self.iam.region()
        self.github_org      = 'filetrust'
        self.source_version  = 'master'
        self.build_spec      = 'buildspec.yml'
        self.docker_type     = 'LINUX_CONTAINER'
        #self.docker_image    = '{0}.dkr.ecr.eu-west-1.amazonaws.com/osbot-jupyter:latest'.format(self.account_id),
        self.compute_type    = 'BUILD_GENERAL1_MEDIUM'
        #self.api             = Create_Code_Build(project_name=self.project_name)
        self.api             = Create_Code_Build(project_name  =self.project_name  , github_org  =self.github_org  ,
                                                 source_version=self.source_version,
                                                 docker_type   =self.docker_type   ,
                                                 compute_type  =self.compute_type  , build_spec  =self.build_spec  )

    #def create_project_with_container__osbot_jupyter(self):
        # kvargs = {
        #     'name'        : self.api.project_name,
        #     'source'      : {'type'                    : 'GITHUB',
        #                      'location'                : self.api.project_repo                 },
        #     'artifacts'   : {'type'                    : 'NO_ARTIFACTS'                    },
        #     'environment' : {'type'                    : 'LINUX_CONTAINER'                  ,
        #                     'image'                    : '{0}.dkr.ecr.eu-west-1.amazonaws.com/osbot-jupyter:latest'.format(self.account_id)     ,
        #                     'computeType'              : 'BUILD_GENERAL1_SMALL'            ,
        #                     'imagePullCredentialsType' : 'SERVICE_ROLE'                    },
        #     'serviceRole' : self.api.service_role
        # }
        # return self.api.code_build.codebuild.create_project(**kvargs)

    # this only needs to run once
    def test_create_policies(self):
        policies = self.api.policies__with_ecr_and_3_secrets()
        self.api.create_role_and_policies(policies)

    def test_create_code_build_and_trigger_first_build(self):
        self.api.code_build.project_delete()
        self.api.create_project_with_container__gs_docker_codebuild()
        #self.create_project_with_container__osbot_jupyter()
        #self.api.code_build.build_start()

    def test_get_task_details(self):
        from osbot_aws.apis.Logs import Logs


        def find_starts(array, text):
            return [item for item in array if item.startswith(text)]

        def find_in(array, text):
            return [item for item in array if text in item]

        #build_id = 'OSBot-Jupyter:a553dda5-953a-41b8-ae91-e068cba4f56b'

        result      = self.api.code_build.project_builds_ids(self.api.project_name)
        build_id    = result.__next__()        # get last one
        build_info  = self.api.code_build.build_info(build_id)
        group_name  = build_info.get('logs').get('groupName')
        stream_name = build_info.get('logs').get('streamName')
        #Dev.pprint(group_name,stream_name)
        logs        = Logs(group_name = group_name , stream_name = stream_name)

        messages= logs.messages()
        #ngrok_messages = find_starts(messages,'t=')
        ngrok_url      = find_in(messages, 'name=command_line addr')[0].split('url=')[1].strip()
        jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()

        Dev.pprint("{0}?token={1}".format(ngrok_url,jupyter_token))



