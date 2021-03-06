from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Lambda import Lambda
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from osbot_jupyter.api.Live_Notebook import Live_Notebook
from osbot_utils.utils import Misc
from osbot_utils.utils.Dev import Dev


def send_message(message, channel, team_id):
    if channel:
        slack_message(message, [], channel, team_id)
    else:
        print(message)
        return message

class Jupyter_Commands:         #*params = (team_id=None, channel=None, params=None)

    api_version = 'v0.40 (GW Bot)'

    @staticmethod
    def files(team_id=None, channel=None, params=None):
        event    = params.pop()                             # needed due to injection of event param
        short_id = Misc.array_pop(params,0)
        target   = " ".join(params)
        if short_id is None:
            return send_message(":red_circle: missing `short id`. The syntax for this method is `contents {short_id} [{path}]`", channel, team_id)
        notebook = Live_Notebook(short_id=short_id)
        text_title, text_body = notebook.files(target)
        attachments = [{'text':text_body, 'color':'good'}]
        slack_message(text_title, attachments,channel,team_id)

    @staticmethod
    def screenshot(team_id=None, channel=None, params=None):
        event = params.pop()                                # needed due to injection of event param
        try:
            if len(params) < 2:
                return send_message(":red_circle: missing `short id` and `path`. The syntax for this method is `screenshot {short_id} {path}`",channel, team_id)
            max_screenshot_delay = 15
            short_id = params.pop(0)
            path     = params.pop(0).replace('<', '').replace('>', '')  # fix extra chars added by Slack
            width    = Misc.to_int(Misc.array_pop(params, 0))
            height   = Misc.to_int(Misc.array_pop(params, 0))
            delay    = Misc.to_int(Misc.array_pop(params, 0))
            if not width : width = 1200
            if not height: height = 800
            if not delay : delay = 0
            if delay > max_screenshot_delay : delay = max_screenshot_delay

            send_message(":point_right: taking screenshot of notebook `{0}` in server `{1}` with width `{2}`, (min) height `{3}` and delay `{4}`".format(path,short_id,width,height,delay),channel,team_id)
            payload = {'short_id': short_id, 'path': path,'width': width,'height': height, 'delay' : delay}
            png_data = Lambda('osbot_jupyter.lambdas.screenshot').invoke(payload)
            if len(png_data) == 3:
                send_message(":red_circle: error taking screenshot :{0} ".format(png_data),channel,team_id)
            else:
                send_message(":point_right: got screenshot with size `{0}` (sending it to slack) ".format(len(png_data)),channel,team_id)
                Lambda('gw_bot.lambdas..png_to_slack').invoke({'png_data': png_data, 'team_id': team_id, 'channel': channel})
        except Exception as error:
            send_message(":red_circle: error in screenshot: {0}".format(error),channel,team_id)

        #slack_message('got image with size {0}'.format(len(png_data)),channel, team_id)
        #return {'png_data': png_data, 'team_id': team_id, 'channel': channel}

    @staticmethod
    def servers(team_id=None, channel=None, params=None):
        text         = ":point_right: Here are the running servers:"
        servers_text = ""
        attachments = []
        for build_id,build in CodeBuild_Jupyter_Helper().get_active_builds().items():
            #print(build_id)
            build_info = build.build_info()
            Dev.pprint(build_info)
            variables = {}
            for variable in build_info.get('environment').get('environmentVariables'):
                variables[variable.get('name')] = variable.get('value')

            repo_name  = variables.get('repo_name')
            user       = variables.get('user')
            timeout    = build_info.get('timeoutInMinutes')
            small_id   = build_id[-5:]
            server_url = build.url()

            if server_url is None:
                user_text = "(server booting up)"
            else:
                user_text = "<{0}|open>".format(server_url)
            #    servers_text += "*{0}*: booting up\n".format(repo_name, server_url)
            #else:
            time = "{0}".format(build_info.get('startTime').strftime("%H:%M"))
            servers_text += "*{1}*: {2} (id: `{0}`, user: <@{3}>, started: {4}, timeout: {5})\n".format(
                                small_id, repo_name,user_text,user,time, timeout)

        if servers_text:
            attachments.append({"text":servers_text, 'color': 'good'})
            slack_message(text, attachments, channel, team_id)
        else:
            slack_message(":information_source: there are no servers running! Why don't you start one using the command `jupyter start {repo name}` ", [], channel, team_id)

        #return "{0}".format(list(CodeBuild_Jupyter_Helper().get_active_builds().keys()))

    @staticmethod
    def start(team_id=None, channel=None, params=None):
        try:
            server_size = 'large'
            event       = Misc.array_pop(params)
            user        = Misc.get_value(event,'data', {}).get('user')
            repo_name   = Misc.array_pop(params,0)

            if repo_name is None:
                repo_name = 'gwbot-jupyter-notebooks'                   # todo: move to global param value
                #return ":red_circle: you need to provide an git repo with notebooks, for example try `gs-notebook-gscs`"
            if '-' not in repo_name and len(repo_name) < 10:
                repo_name = 'gs-notebook-{0}'.format(repo_name)         # todo: move to config value (since this is implementation specific)
            payload = {
                        'repo_name': repo_name,
                        "channel"  : channel  ,
                        'user'     : user     ,
                        'server_size': server_size}
            #slack_message(f':point_right: about to start a jupyter notebook with params: {payload} ', [], channel)
            Lambda('osbot_jupyter.lambdas.start_server').invoke_async(payload)
        except Exception as error:
            return f':red_circle: error in Jupyter start command: {error}'


    @staticmethod
    def stop_all(*params):
        return CodeBuild_Jupyter_Helper().stop_all_active()

    @staticmethod
    def stop(team_id=None, channel=None, params=None):
        short_id = params.pop(0)
        notebook = Live_Notebook().set_build_from_short_id(short_id)
        if notebook:
            notebook.stop()
            return ':point_right: stopped server with id: `{0}`'.format(short_id)
        return ':red_circle: error: could not find server with id: `{0}`'.format(short_id)

    @staticmethod
    def web(team_id=None, channel=None, params=None):
        #event = Misc.array_pop(params)
        params = {'team_id':team_id, 'channel': channel, 'params':params}
        Lambda('osbot_jupyter.lambdas.jupyter_web').invoke_async(params)

    @staticmethod
    def version(*params):
        return Jupyter_Commands.api_version
