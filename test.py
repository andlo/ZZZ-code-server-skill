import os
import tarfile
import subprocess
import signal
import urllib.request
import tarfile
import platform
import requests


try:
        SafePath = '/home/pi/WORK/test'
        pf = platform.machine()
        if pf is 'armv71':
            url = 'https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-armv7l.tar.gz'
        elif pf is 'arm64':
            url = 'https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-arm64.tar.gz'
        elif pf is 'amd64':
            url = 'https://github.com/coder/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-amd64.tar.gz'
        else:
            return
        r = requests.get(url)
        open(r.)
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
