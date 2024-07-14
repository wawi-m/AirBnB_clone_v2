#!/usr/bin/python3
"""Creates a comperessed_static folder"""
import os
from datetime import datetime
from fabric.api import local, run, put, env
env.hosts = ['54.174.243.255', '54.208.245.251']


# Creates a comperessed_static folder
def do_pack():
    """Creates a .tgz archive compressing its contents web_static folder"""
    try:
        local("mkdir -p versions")
        p_name = "web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf versions/{} web_static".format(p_name))
        return ("versions/{}".format(p_name))
    except Exception:
        return None


# distributes an archive to web servers
def do_deploy(archive_path):
    """ that distributes an archive to web servers
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
        run("sudo ln -sf\
            /data/web_static/releases/test /data/web_static/current")
        run("cp -r \
            /data/web_static/current/web_static/* /data/web_static/current/")
        return True
    except Exception:
        return False
