#!/usr/bin/python3
""" the script that contains the necessary functions for deploying a
    website to a remote server
"""
from fabric.api import local, env, put, run, cd, lcd
from datetime import datetime
from os.path import exists
user = local('whoami', capture=True)
env.hosts = ['52.55.249.213', '54.157.32.137']
#  env.hosts = ['3.84.255.85', '100.25.171.58']


def do_pack():
    """ the function creates a tarball zip file (tgz) from the
        contents of the web_static directory
    """
    env.user = user
    zip_file_name = datetime.now().strftime("web_static_%Y%m%d%H%M%S")
    target_folder = 'versions'
    source_folder = 'web_static'
    print(type(zip_file_name))

    #  ensure the target folder exists and create it if it does not
    if not exists(target_folder):
        local(f'mkdir -r {target_folder}')
    #  make the archive file
    local(f'tar -czvf {target_folder}/{zip_file_name}.tgz {source_folder}')

    if exists(f'{target_folder}/{zip_file_name}.tgz'):
        return f'{target_folder}/{zip_file_name}.tgz'
    else:
        return False


def do_deploy(archive_path):
    """ function deploys an archive in the versions directory to a server
    """
    env.user = user
    archive_name = archive_path.split('/')[-1]
    archive_name_no_extension = archive_name.split('.')[0]
    link = '/data/web_static/current'
    dest_folder = f'/data/web_static/releases/{archive_name_no_extension}'

    if not exists(f'{archive_path}'):
        return False
    flag = local(f"if [ ! -d {dest_folder} ]; then echo 'True'; fi")
    if flag:
        local(f'sudo mkdir -p {dest_folder}')
    else:
        local(f'sudo rm -rf {dest_folder}')
        local(f'sudo mkdir -p {dest_folder}')
    local(f'sudo mv {archive_path} /tmp/{archive_name}')
    with lcd(f"{dest_folder}"):
        local(f'sudo tar -xzf /tmp/{archive_name}')
    local(f'sudo rm /tmp/{archive_name}')
    flag = local(f"if [ ! -f {link} ]; then echo 'True'; fi")
    if flag:
        pass
    else:
        local('sudo rm -rf /data/web_static/current')
    local(f'sudo mv {dest_folder}/web_static/* {dest_folder}')
    local(f'sudo rm -rf {dest_folder}/web_static')
    local(f'sudo ln -sf {dest_folder} {link}')

    return True
