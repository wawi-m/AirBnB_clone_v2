#!/usr/bin/python3
"""Creates a .tgz archive compressing its contents web_static folder."""
from fabric.api import local
import time


def do_pack():
    """Creates a .tgz archive compressing its contents web_static folder"""
    try:
        local("mkdir -p versions")
        p_name = "web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf versions/{} web_static".format(p_name))
        return ("versions/{}".format(p_name))
    except Exception:
        return None
