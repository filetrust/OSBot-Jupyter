from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_API import Jupyter_API
from osbot_jupyter.api.Jupyter_Web_Cell import Jupyter_Web_Cell
from osbot_jupyter.api.Jypyter_API_Actions import Jupyter_API_Actions


class test_jupyter_dev_coding(TestCase):

    def setUp(self):
        self.headless       = False
        self.server         = 'http://localhost:8888'
        self.image_name     = 'jupyter/datascience-notebook:9b06df75e445'
        self.notebook_name  = 'work/test-1.ipynb'
        self.docker_jp      = Docker_Jupyter(self.image_name)
        self.token          = self.docker_jp.token()
        self.jp_api         = Jupyter_API_Actions(server=self.server, token=self.token)
        self.jp_web         = Jupyter_Web_Cell(token=self.token, headless=self.headless)
        self.jp_cell        = Jupyter_Web_Cell(token=self.token, headless=self.headless)
        self.notebook_name  = 'dev_coding'
        self.notebook_path  = '{0}.ipynb'.format(self.notebook_name)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_open_dev_notebook(self):
        if self.jp_api.notebook_exists(self.notebook_path) is False:
            self.jp_api.create_notebook(notebook_name=self.notebook_name)
        self.jp_web.open_notebook_edit(self.notebook_name)

    def test_set_dev_environment(self):
        code = "%load_ext autoreload\n%autoreload 2"
        self.jp_cell.execute_python(code)
        self.jp_cell.delete()

    def test_run_code(self):
        code = """
from osbot_jupyter.notebook.Widgets import Widgets
Widgets().ping()
        """

        self.jp_cell.execute_python(code, new_cell=False)


    def test_add_code_hide_button(self):
        code = """
from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')        
"""

        self.jp_cell.execute_python(code, new_cell=True)