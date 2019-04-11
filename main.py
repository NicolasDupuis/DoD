import cherrypy
import pandas as pd
import os
import subprocess
import socket
import time

# Run external command, returns stdout
def externalCmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

# Run external command
def externalCmdLive(cmd):
    # convert string into list of words
    _cmd = [word for word in cmd.split(" ")]
    return subprocess.run(_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

# Return a open port number, to be used by a new container
def getNewPort():
    # let's use from 8500 to 8900
    for port in range(8500, 8900):
        # Test if the port is already opened
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex(('127.0.0.1', port)) != 0:  # oh good, it's open, let's use that one
            sock.close()
            break
    return port


class Glob(object):
    ''' Global variables '''
    def __init__(self):

        self.internerBrowser = "firefox"
        self.terminal = "xterm -e "  # to run external commands in a terminal

        self.roles = ["User", "Admin"]

        self.users = {}
        self.users["Jordan"] = self.roles[1]
        self.users["Nicolas"] = self.roles[0]
        self.users["Andy"] = self.roles[0]

        self.userpassword = {}
        self.userpassword["Nicolas"] = "_nicolas"
        self.userpassword["Andy"] = "_andy"
        self.userpassword["Jordan"] = "_jordan"

        # Images details, to be controlled by the admin. Will end up in a database.
        self.images = {}

        self.images["rocker/rstudio"] = {"mountDefault": "None",
                                         "validated": True,
                                         "password": True,
                                         "exposedPort": 8787,
                                         "webapp": True,
                                         "nickname": "Rstudio",
                                         "mountPoint": "/home/rstudio/"}

        self.images["jupyter/scipy-notebook"] = {"mountDefault": "None",
                                                 "validated": False,
                                                 "exposedPort": 8888,
                                                 "webapp": True,
                                                 "password": False,
                                                 "mountPoint": "/home/jovyan/",
                                                 "forceGID": "1000",
                                                 "user": "root",
                                                 "postadd": "start-notebook.sh --NotebookApp.token='abcd12345'",
                                                 "addURL": "?token=<token>",
                                                 "nickname": "Jupyter"}

        self.images["r-base"] = {"mountDefault": "None",
                                 "validated": False,
                                 "nickname": "R",
                                 "exposedPort": None,
                                 "webapp": False,
                                 "password": False,
                                 "mountPoint": "/media/"}

        self.images["alpine"] = {"mountDefault": "None",
                                 "validated": False,
                                 "nickname": "Alpine",
                                 "exposedPort": None,
                                 "webapp": False,
                                 "password": False,
                                 "mountPoint": "/media/"}

        self.images["hello-world"] = {"mountDefault": "None",
                                      "validated": False,
                                      "nickname": "Hello World!",
                                      "exposedPort": None,
                                      "webapp": False,
                                      "password": False}


class Webpages(object):
    # HTTP request objects

    def index(self):
        html_code = header_layout()
        html_code += topContainer_Layout()

        html_code += '''<br><br><br><br>          

                <center><img src="/static/d-wise-logo.jpg" alt="Logo" style="width:300px;border:0;">
                 <form action ="/login" method = GET>
                  <h4><strong><i>'on demand'</strong></i></h4>
                  <h5> - a prototype by Nicolas and Andy -</h3><br>
                <table style="width:30%">
                  <tr>
                    <th>Name</th>
                    <td><td><input name = "username"></td>
                  </tr>
                  <tr>
                    <th>Password</th>
                    <td><td><input type="password" name="userpassword"></td>
                  </tr>
                </table><br>
                <input type=submit class="button" value="Login">

                 </form>          
                 <p><a href="http://www.d-wise.com">Visit d-wise.com!</a></p></center>'''

        html_code += footer_layout()

        return html_code

    index.exposed = True

    def login(self, username, userpassword):
        self.userpassword = userpassword
        self.username = username
        if self.username not in glob.users:
           html_code = "Unregistered user"
        elif self.userpassword != glob.userpassword[self.username]:
            html_code = "Wrong password"
        else:
            self.role = glob.users[self.username]

            # build welcome page
            html_code  = header_layout()
            html_code += topContainer_Layout()
            html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
            html_code += dockerImages_layout(self.username, role=self.role)
            html_code += footer_layout()
        return html_code
    login.exposed = True


    # Docker Images
    ########################################################################

    # Page listing all the docker images in the local library
    def dockerlibrary(self, image=None):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImages_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    dockerlibrary.exposed = True


    # Display the details of a specific image
    def imageDetails(self, image):
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImagesDetails_layout(role=self.role, image=image)
        html_code += footer_layout()
        return html_code
    imageDetails.exposed = True

    def imageSettings(self, **kwargs):

        image = kwargs["image"]
        for item in list(kwargs.keys()):
            if item != "image":
                glob.images[image][item] = kwargs[item]

        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImagesDetails_layout(role=self.role, image=image)
        html_code += footer_layout()
        return html_code
    imageSettings.exposed = True

    # Display the details of a specific image
    def imageLaunchPad(self, **kwargs):

        image, mode = kwargs["image"], kwargs["mode"]

        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")


        if mode == "configure":
            html_code += imageLaunchPad_layout(image=image)

        elif mode == "now":  # use default and create the image now

            if glob.images[image]["mountDefault"] != "None":
                volume = glob.images[image]["mountDefault"]
                mountPoint = glob.images[image]["mountPoint"]
            else:
                volume = None
                mountPoint = None

            # run!
            dockerAPI.instantiatelImage(image,
                                        role=self.role,
                                        volume=volume,
                                        mountPoint=mountPoint,
                                        username=self.username,
                                        userpassword=self.userpassword)

            html_code += dockerInstances_layout(self.username, role=self.role)

        html_code += footer_layout()
        return html_code
    imageLaunchPad.exposed = True

    # Questions when cloning an image
    def cloneImageinfo(self, **kwargs):
        container_name, container_id = kwargs["name"], kwargs["id"]
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += imageClone_layout(container_name=container_name, container_id=container_id)
        html_code += footer_layout()
        return html_code
    cloneImageinfo.exposed = True

    def cloneImage(self, **kwargs):
        dockerAPI.cloneImage(container_id=kwargs["container_id"], newimage=kwargs["newimage"], tag=kwargs["tag"])
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImages_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    cloneImage.exposed = True


    # Display the details of a specific image
    def deleteImage(self, image):
        dockerAPI.removeImage(image)
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImages_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    deleteImage.exposed = True

    # Display the details of a specific image
    def pullImage(self, image):
        dockerAPI.pullImage(image)
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImages_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    pullImage.exposed = True

    # Actions on Docker images: remove, instantiate, pull
    def actionsImage(self, **kwargs):

        print("KWARGS: " + str(kwargs))

        # unpack parameters
        image = kwargs['run'].split("&")[0].split("=")[1]
        volume = kwargs['run'].split("&")[1].split("=")[1]
        mountPoint = kwargs['mountPoint']
        cpu = kwargs['cpu']
        ram = kwargs['ram']

        # create the image
        dockerAPI.instantiatelImage(image,
                                    role=self.role,
                                    username=self.username,
                                    userpassword=self.userpassword,
                                    volume=volume,
                                    mountPoint=mountPoint,
                                    cpu=cpu,
                                    ram=ram)
        # display !
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")
        html_code += dockerInstances_layout(self.username, role=self.role)
        html_code += footer_layout()

        # user asked to remember the choice made.
        try:
            if kwargs["remember"] == "True":
                glob.images[image]["mountPoint"] = mountPoint
                glob.images[image]["mountDefault"] = volume

                print(glob.images[image]["mountDefault"])
                print(glob.images[image]["mountPoint"])
        except:
            pass
        return html_code
    actionsImage.exposed = True

    ########################################################################
    # Docker Instances
    ########################################################################

    # page listing all the docker containers available
    def dockerInstances(self):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")
        html_code += dockerInstances_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    dockerInstances.exposed = True

    # Display detailed info on a specific active container
    def instanceDetails(self, container_id):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")
        html_code += dockerInstanceDetails_layout(container_id=container_id)
        html_code += footer_layout()
        return html_code
    instanceDetails.exposed = True

    # Actions on an active Docker instances: stop, pause, unpause, restart or get lower level details
    def actionsInstance(self, **kwargs):

        action = list(kwargs.keys())[0]
        container_id = kwargs[action]

        if action == "open":
            dockerAPI.openInstance(container_id)
        elif action == "stop":
            dockerAPI.stopInstance(container_id)
        elif action == "pause":
            dockerAPI.pauseInstance(container_id)
        elif action == "unpause":
            dockerAPI.unpauseInstance(container_id)
        elif action == "restart":
            dockerAPI.restartInstance(container_id)

        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")
        if action == "details":
            html_code += dockerInstances_layout(self.username, role=self.role, container_id=container_id)
        else:
            html_code += dockerInstances_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    actionsInstance.exposed = True

    ########################################################################
    # Volumes library
    ########################################################################

    # page listing all the docker volumes available
    def volumeslibrary(self):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        html_code += dockerVolumes_layout()
        html_code += footer_layout()
        return html_code
    volumeslibrary.exposed = True

    # Details on a specific volume
    def volumeDetails(self, volume):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        html_code += volumeDetails_layout(volume=volume)
        html_code += footer_layout()
        return html_code
    volumeDetails.exposed = True

    # Create a volume
    def createVolume(self, **kwargs):

        dockerAPI.createVolume(volume=kwargs["volume"], root_password=kwargs["root_password"])

        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        html_code += dockerVolumes_layout()
        html_code += footer_layout()
        return html_code
    createVolume.exposed = True

    # Actions on an active Docker instances: stop, pause, unpause, restart or get lower level details
    def actionsVolume(self, **kwargs):

        action, volume = kwargs["action"], kwargs["volume"]

        if action == "details":
            dockerAPI.volumeDetails(volume)
        elif action == "delete":
            dockerAPI.deleteVolume(volume)

        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        if action == "details":
            html_code += volumeDetails_layout(volume=volume)
        else:
            html_code += dockerVolumes_layout()
        html_code += footer_layout()
        return html_code
    actionsVolume.exposed = True


# Global objects
glob = Glob()

# load HTML modules
exec(open('HTML_modules.py').read(), globals())

# load docker object
exec(open('docker_API.py').read(), globals())
dockerAPI = DockerAPI()

# run web server
cherrypy.engine.exit()
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        },
        '/favicon.ico':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename:': './static/favico.jpeg'
            }

    }
    cherrypy.quickstart(Webpages(), '/', conf)