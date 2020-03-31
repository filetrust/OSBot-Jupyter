from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper


class test_CodeBuild_Jupyter_Helper(Test_Helper):
    def setUp(self):
        super().setUp()
        self.api    = CodeBuild_Jupyter_Helper()
        self.result = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test_get_active_build_id(self):
        self.result = self.api.get_active_build_id()

    def test_get_active_builds(self):
        builds = self.api.get_active_builds()
        print()
        for id, build in builds.items():
            #assert build.build_status() == 'IN_PROGRESS'
            #assert build.build_phase() == 'BUILD'             # need to improve the resilience of this test
            print(id, build.build_status() , build.build_phase())

    def test_start_build(self):
        result = self.api.start_build()
        Dev.pprint(result.build_info())

    def test_start_build_and_wait_for_jupyter_load(self):
        result = self.api.start_build_and_wait_for_jupyter_load()
        Dev.pprint(result.build_status())


    def test_start_build_for_repo__server_size(self):
        repo = 'gs-notebook-gscs'
        self.api.start_build_for_repo(repo, server_size = 'small' )
        self.api.start_build_for_repo(repo, server_size = 'medium')
        self.api.start_build_for_repo(repo, server_size = 'large' )

    def test_start_build_for_repo_and_wait_for_jupyter_load(self):
        repo = 'gwbot-jupyter-notebooks'
        self.result = self.api.start_build_for_repo_and_wait_for_jupyter_load(repo)


    def test_stop_all_active(self):
        result = CodeBuild_Jupyter_Helper().stop_all_active()
        Dev.pprint("stopped builds {0}".format(result))

    def test_save_active_server_details(self):
        tmp_file    = '/tmp/active_jupyter_server.yml'
        self.result = self.api.save_active_server_details(tmp_file)


    def test_gw_repo_start_build_for_repo__server_size(self):
        repo_name = 'gwbot-jupyter-notebooks'
        self.result = self.api.start_build_for_repo(repo_name, server_size = 'medium' )
