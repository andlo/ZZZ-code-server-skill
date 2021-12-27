"""
skill code-server
Copyright (C) 2022  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sys import platform
from mycroft import MycroftSkill, intent_file_handler
import os
import tarfile
import subprocess
import signal
import urllib.request
import tarfile
import platform
#from psutil import virtual_memory

class CodeServer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.log.info("Initialize code-server...")
        if (self.settings.get("workspace") is not True or
                self.settings.get("workspace") == ''):
            self.settings["workspace"] = str(self.config_core.get('data_dir') +
                                             '/' +
                                             self.config_core.get('skills', {})
                                             .get('msm', {})
                                             .get('directory'))

        if (self.settings.get("code-server installed") is not True or
                self.settings.get("code-server installed") is None):
            self.install_code()
        if not self.pid_exists(self.settings.get("code_pid")):
            self.settings["code_pid"] = None
        if (self.settings.get("auto_start") and
                self.settings.get("code_pid") is None):
            self.run_theia()

    @intent_file_handler('server.code.intent')
    def handle_server_code(self, message):
        self.speak_dialog('server.code')

    @intent_file_handler('stop.intent')
    def handle_ide_stop(self, message):
        if self.stop_theia():
            self.speak_dialog('code_stopped')
        else:
            self.speak_dialog('code_is_not_running')

    @intent_file_handler('start.intent')
    def handle_ide_start(self, message):
        url = os.uname().nodename + " kolon 3000"
        if self.run_theia():
            self.speak_dialog('code_started', data={"url": url})
        else:
            self.speak_dialog('code_already_running', data={"url": url})

    @intent_file_handler('restart.intent')
    def handle_ide_restart(self, message):
        url = os.uname().nodename + " kolon 3000"
        self.stop_code()
        if self.start_code():
            self.speak_dialog('code_started', data={"url": url})

    def start_code(self):
        self.log.info("Stopping code-server")
        SafePath = self.file_system.path
        if self.settings.get("code_pid") is not None:
            try:
                os.killpg(self.settings.get("code_pid"), signal.SIGTERM)
            except Exception:
                #proc = subprocess.Popen('pkill -f "yarn theia start"',
                #                        cwd=SafePath,
                #                        preexec_fn=os.setsid,
                #                        shell=True)
                #proc.wait()
                #self.settings["code_pid"] = None
            return True
        else:
            return False

    def run_code(self):
        if self.settings.get("code_pid)") is None:
            self.log.info("Starting code-server")
            SafePath = self.file_system.path
            #theia_proc = subprocess.Popen(SafePath + '/theia_run.sh ' +
            #                              self.settings.get("workspace") +
            #                              ' >/dev/null 2>/dev/null ',
            #                              cwd=SafePath,
            #                              preexec_fn=os.setsid, shell=True)
            #self.settings["code_pid"] = theia_proc.pid
            return True
        else:
            return False

    def install_code(self):
        try:
            SafePath = self.file_system.path
            pf = platform.machine
            if pf = 'armv71':
                url = https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-armv7l.tar.gz
            elif pf = 'arm64':
                url = https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-arm64.tar.gz
            elif pf = 'amd64':
                url = https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-amd64.tar.gz
            else:
                self.log.info('Platform ' + pf + 'code-server cant run on a this device')
                self.speak_dialog('platform_not_supported')
                self.settings['code installed'] = 'False'
                return
            download = urllib.request.urlretrieve(url)
            file = tarfile.open(download)
            file.extractall(SafePath + '\code-server')
            file.close()
            os.remove(file)
            self.log.info("Installed OK")
            self.settings['code installed'] = 'True'
            self.speak_dialog('installed_OK')
            return True
        except Exception:
            self.log.info("Code is not installed - something went wrong!")
            self.settings['code installed'] = 'False'
            self.speak_dialog('installed_BAD')
            return False

    def pid_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

def create_skill():
    return CodeServer()

