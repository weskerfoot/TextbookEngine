from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
import fabric.operations as op

env.hosts = ["wes@mgoal.ca:444"]

@task
def makeBuild():
    local("rm -fr ./build")
    local("mkdir -p build/{scripts,styles,templates}")

@task
def buildTags():
    local("riot ./src/scripts/ ./build/scripts/tags.js")

@task
def uglify():
    local("uglifyjs ./build/scripts/*js > ./build/scripts/search.min.js")

@task
def sass():
    local("sassc ./src/styles/*scss > ./build/styles/search.min.css")

@task
def copy():
    local("cp -r ./src/scripts/*.js ./build/scripts/")
    local("cp -r ./src/styles/*.css ./build/styles/")
    local("cp -r ./src/templates/*html ./build/templates/")
    local("cp -r ./src/{archive.py,openlibrary.py,search.py,website.py,textbookExceptions.py} ./build/")
    local("cp {search.ini,search.service,requirements.txt} ./build/")

@task
def upload():
    run("mkdir -p ~/tbookbuild")
    rsync_project(local_dir="./build/", remote_dir="~/tbookbuild/", delete=False, exclude=[".git"])

@task
def serveUp():
    sudo("rm -fr /srv/http/build")
    sudo("cp -r /home/wes/tbookbuild /srv/http/build")
    sudo("cp /home/wes/tbookbuild/search.service /etc/systemd/system/search.service")
    sudo("systemctl daemon-reload")
    sudo("systemctl enable search.service")
    sudo("systemctl restart search.service")

@task
def buildVenv():
    with cd("~/tbookbuild"):
        run("virtualenv -p $(which python3) ~/tbookbuild/venv")
        with prefix("source ~/tbookbuild/venv/bin/activate"):
            run("pip3 install -r requirements.txt")

@task
def buildLocalVenv():
    with lcd("~/TextbookEngine/build"):
        local("virtualenv -p $(which python3) ~/TextbookEngine/build/venv")
        with prefix("source ~/TextbookEngine/build/venv/bin/activate"):
            local("pip3 install -r requirements.txt")

@task(default=True)
def build():
    makeBuild()
    buildTags()
    uglify()
    sass()
    copy()
    upload()
    buildVenv()
    serveUp()
