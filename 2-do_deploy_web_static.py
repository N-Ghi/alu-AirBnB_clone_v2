#!/usr/bin/python3

"""Comment"""

from fabric.api import *
import os
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['3.208.21.184', '54.91.88.127']


def do_pack():

    """Comm"""
    
    local("mkdir -p versions")
    result = local("tar -cvzf versions/hbnb_static_{}.tgz hbnb_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result


def do_deploy(archive_path):
    """Comment"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = match.group(0)
    result = put(archive_path, "/tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    # Uncompress the archive to the folder
    #     /data/hbnb_static/releases/<archive filename without extension> on
    #     the web server

    result = run(
        "mkdir -p /data/hbnb_static/releases/{}/".format(archive_filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/hbnb_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False

    # Delete the archive from the web server
    result = run("rm /tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    result = run("mv /data/hbnb_static/releases/{}"
                 "/hbnb_static/* /data/hbnb_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False
    result = run("rm -rf /data/hbnb_static/releases/{}/hbnb_static"
                 .format(archive_filename))
    if result.failed:
        return False

    # Delete the symbolic link /data/hbnb_static/current from the web server
    result = run("rm -rf /data/hbnb_static/current")
    if result.failed:
        return False

    #  Create a new the symbolic link
    #  /data/hbnb_static/current on the web server,
    #     linked to the new version of your code
    #     (/data/hbnb_static/releases/<archive filename without extension>)
    result = run("ln -s /data/hbnb_static/releases/{}/ /data/hbnb_static/current"
                 .format(archive_filename))
    if result.failed:
        return False

    return True
