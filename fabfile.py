from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
import fabric.operations as op

env.hosts = ["wes@mgoal.ca:444"]

@task
def installDeps():
    local("npm install --save-dev rollup rollup-plugin-riot")

@task
def makeBuild():
    local("mkdir -p build/{scripts,styles,templates}")

@task
def buildTags():
    local("riot ./src/scripts/ ./build/scripts/tags.js")

@task
def uglify():
    local("rollup -c rollup.config.js")
    local("uglifyjs ./build/bundle.js > ./build/scripts/search.min.js")

@task
def sass():
    local("sassc ./src/styles/*scss > ./build/styles/search.min.css")

@task
def copy():
    local("cp ./goal.png ./build/goal.png")
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
    sudo("rm -fr /srv/http/goal/scripts/")
    sudo("mkdir -p /srv/http/goal/scripts")
    sudo("mkdir -p /srv/http/goal/styles")
    sudo("cp -r /home/wes/tbookbuild /srv/http/build")
    sudo("cp -r /home/wes/tbookbuild/scripts/*js /srv/http/goal/scripts/")
    sudo("cp -r /home/wes/tbookbuild/styles/*css /srv/http/goal/styles/")
    sudo("cp /home/wes/tbookbuild/search.service /etc/systemd/system/search.service")
    sudo("cp /home/wes/tbookbuild/goal.png /srv/http/goal/goal.png")
    sudo("systemctl daemon-reload")
    sudo("systemctl enable search.service")
    sudo("systemctl restart search.service")

@task
def serveUpLocal():
    local("sudo rm -fr /srv/http/build")
    local("sudo rm -fr /srv/http/goal/scripts/")
    local("sudo mkdir -p /srv/http/goal/scripts")
    local("sudo cp -r /home/wes/TextbookEngine/build/ /srv/http/build")
    local("sudo cp -r /home/wes/TextbookEngine/build/scripts/*js /srv/http/goal/scripts/")
    local("sudo cp -r /home/wes/TextbookEngine/build/styles/*css /srv/http/goal/styles/")
    local("sudo cp /home/wes/TextbookEngine/goal.png /srv/http/goal/goal.png")
    local("sudo cp /home/wes/TextbookEngine/build/search.service /etc/systemd/system/search.service")
    local("sudo systemctl daemon-reload")
    local("sudo systemctl enable search.service")
    local("sudo systemctl restart search.service")

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
    copy()
    buildTags()
    uglify()
    sass()
    upload()
    buildVenv()
    serveUp()

@task
def buildLocal():
    makeBuild()
    copy()
    buildTags()
    uglify()
    sass()
    buildLocalVenv()
    serveUpLocal()
