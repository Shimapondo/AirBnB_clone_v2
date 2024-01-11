#!/usr/bin/python3
""" the script that contains the necessary functions for deploying a
    website to a remote server
"""
from fabric.api import local, env
from datetime import datetime


def do_pack():
    """ the function creates a tarball zip file (tgz) from the
        contents of the web_static directory
    """
    env.user = local('whoami', capture=True)
    zip_file_name = datetime.now().strftime("web_static_%Y%m%d%H%M%S")
    target_folder = 'versions'
    source_folder = 'web_static'

    #  ensure the target folder exists and create it if it does not
    local(f'if [ ! -d {target_folder} ]; then\
            mkdir {target_folder};\
            fi')
    #  make the archive file
    local(f'tar -czvf {target_folder}/{zip_file_name}.tgz {source_folder}')
