#!/bin/bash
get_latest_release() {
#  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
#    grep '"tag_name":' |                                            # Get tag line
#    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
#}
curl --silent "https://api.github.com/repos/$1/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")'
}
# Usage
# $ get_latest_release "coder/code-server"
# v0.31.4
get_latest_release "coder/code-server"