from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jupyter.api_notebook.Jp_Graph_Data import Jp_Graph_Data


class test_Jp_Graph_Data(TestCase):

    def setUp(self):
        self.jp_graph_data = Jp_Graph_Data()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_issue(self):
        issue_id = 'RISK-12'
        assert self.jp_graph_data.issue(issue_id).get('Key') == issue_id

    def test_issues(self):
        issues_ids = ['RISK-12','RISK-234']
        self.result = list(set(self.jp_graph_data.issues(issues_ids))) == issues_ids


    def test_jira_links(self):
        depth         = 1
        key           = 'PERSON-1'
        graph  = self.jp_graph_data.jira_links(key, depth)
        assert len(graph.nodes) > 5
        assert len(graph.edges) > 5

    def test_jira_search(self):
        assert len(self.jp_graph_data.jira_search('people di*')) > 10

    def test_graph_expand(self):
        depth         = 1
        key           = 'RISK-1610'
        link_types    = 'has RISK'
        graph  = self.jp_graph_data.graph_expand(key, depth, link_types)

        assert len(graph.nodes) == 7
        assert len(graph.edges) == 6

    def test_run_with_trace(self):
        from osbot_utils.decorators.trace.Trace_Call import Trace_Call
        self.result = Trace_Call().invoke_method(test_Jp_Graph_Data.test_graph_expand, self)
