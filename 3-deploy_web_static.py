#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers using deploy()
"""

from fabric.api import env, local, run, put
from datetime import datetime
import os

env.hosts = ['54.174.243.255', '54.208.245.251']


def do_pack():
    """Creates a .tgz archive compressing its contents web_static folder"""
    try:
        local("mkdir -p versions")
        p_name = "web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf versions/{} web_static".format(p_name))
        return ("versions/{}".format(p_name))
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        file_name_no_ext = file_name.split(".")[0]
        run("sudo chown -R $USER:$USER /data/")
        run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(file_name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, file_name_no_ext))

        run("rm /tmp/{}".format(file_name))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name_no_ext))
        run("sudo ln -sf /data/web_static/releases/test \
            /data/web_static/current")
        run(" cp /data/web_static/current/web_static/* \
            /data/web_static/current/")
        return True
    except Exception:
        return False


def deploy():
    """
    deploys full project
    """
    path = do_pack()
    if path is not None:
        return do_deploy(path)
    return False
