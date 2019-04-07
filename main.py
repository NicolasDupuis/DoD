import cherrypy
import pandas as pd
import os
import subprocess
import socket

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

        self.roles = ["User", "Admin"]

        self.users = {}
        self.users["Jordan"] = self.roles[1]
        self.users["Nicolas"] = self.roles[0]
        self.users["Andy"] = self.roles[0]

        self.userpassword = {}
        self.userpassword["Nicolas"] = "_nicolas"
        self.userpassword["Andy"] = "_andy"
        self.userpassword["Jordan"] = "_jordan"

        # For a given image, 1) how to instantiate the container 2) launch in web browser if possible
        self.launchCommands = {}
        self.launchCommands["rocker/rstudio"] = ["docker run --name <userid>_rstudio<#n#> --rm -dp <port>:8787 -e PASSWORD=<password> rocker/rstudio", self.internerBrowser + " http://127.0.0.1:<port>/", "rstudio"]
        self.launchCommands["jupyter/scipy-notebook"] = ["docker run --name <userid>_Jupyter<#n#> -dp <port>:8888 jupyter/scipy-notebook", self.internerBrowser + " 127.0.0.1:<port>/?token=<token>", "Jupyter"]
        self.launchCommands["r-base"] = ['konsole -e docker run --name <userid>_r<#n#> -ti --rm r-base', "R"]
        self.launchCommands["alpine"] = ["konsole -e docker run --name <userid>_alpine<#n#> -ti --rm alpine", "Alpine"]
        self.launchCommands["hello-world"] = ["konsole -e docker run --name <userid>_Helloworld<#n#> -ti --rm hello-world", "HelloWorld"]

        self.ports = []

class Webpages(object):
    # HTTP request objects

    def index(self):

        html_code = header_layout()
        html_code += topContainer_Layout()

        html_code += '''<br><br><br><br>  
        
        
        <center><img src="/static/d-wise-logo.jpg" alt="Logo" /><br>
         <form action ="/login" method = GET>
          <h3> Welcome to <strong>d-wise on demand </strong></h3>
          <h5> - a prototype by Nicolas and Andy -</h3>
          
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
        if image != None:
            html_code += dockerImages_layout(self.username, role=self.role,image=image)
        else:
            html_code += dockerImages_layout(self.username, role=self.role)
        html_code += footer_layout()
        return html_code
    dockerlibrary.exposed = True


    # Display the details of a specific image
    def imageDetails(self, image):
        html_code = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")
        html_code += dockerImagesDetails_layout(image=image)
        html_code += footer_layout()
        return html_code
    imageDetails.exposed = True


    # Actions on Docker images: remove, instantiate, pull
    def actionsImage(self, **kwargs):

        html_code  = header_layout()
        html_code += topContainer_Layout()
        actions, image = list(kwargs.keys())[0].split("_")

        if actions in ["pull", "delete", "details"]:
            html_code += sidebar_layout(role=self.role, username=self.username, current="dockerlibrary")

            if actions == "pull":
                dockerAPI.pullImage(kwargs["pull_na"])
                html_code += dockerImages_layout(self.username, role=self.role)
            elif actions == "delete":
                dockerAPI.removeImage(image)
                html_code += dockerImages_layout(self.username, role=self.role)
            elif actions == "details":
                html_code += dockerImages_layout(self.username, role=self.role, image=image)

        elif actions == "run":
            dockerAPI.instantiatelImage(image, role=self.role, username = self.username, userpassword=self.userpassword)
            html_code += sidebar_layout(role=self.role, username=self.username, current="dockerInstances")
            html_code += dockerInstances_layout(self.username, role=self.role)

        html_code += footer_layout()
        return html_code
    actionsImage.exposed = True


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


    # Volumes library
    ########################################################################

    # page listing all the docker volumes available
    def volumeslibrary(self, volume_id=None):
        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        if volume_id == None:
            html_code += dockerVolumes_layout(self.username, role=self.role)
        else:
            html_code += dockerVolumes_layout(self.username, role=self.role, volume_id=volume_id)
        html_code += footer_layout()
        return html_code
    volumeslibrary.exposed = True

    # Actions on an active Docker instances: stop, pause, unpause, restart or get lower level details
    def actionsVolume(self, **kwargs):

        actions, volume_id = list(kwargs.keys())[0].split("@")

        if actions == "details":
            dockerAPI.volumeDetails(volume_id)
        elif actions == "delete":
            dockerAPI.deleteVolume(volume_id)
        elif actions == "create":
            dockerAPI.createVolume(kwargs["create@na"])

        html_code  = header_layout()
        html_code += topContainer_Layout()
        html_code += sidebar_layout(role=self.role, username=self.username, current="volumeslibrary")
        if actions == "details":
            html_code += dockerVolumes_layout(self.username, role=self.role, volume_id=volume_id)
        else:
            html_code += dockerVolumes_layout(self.username, role=self.role)
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
            'tools.staticdir.dir': '/home/nicolas/PycharmProjects/DoD/static'
        }
    }
    cherrypy.quickstart(Webpages(), '/', conf)


