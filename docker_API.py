import docker
import subprocess
from io import StringIO

def externalCmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

class DockerAPI(object):
    ''' Interface with docker '''
    def __init__(self):
        pass

    def longestImageName(self):
        client = docker.from_env()

        if len(client.images.list()) > 0:
            self.images = []
            for self.image in client.images.list():
                self.start = str(self.image).find("'")
                self.end = str(self.image).find(":", self.start + 1)
                self.images.append(str(self.image)[self.start + 1:self.end])
            return max([len(item) for item in self.images])
        else:
            return 0

    def longestContainerName(self):
        client = docker.from_env()

        if len(client.containers.list()) > 0:
            self.containers = []
            for self.container in client.containers.list():
                self.start = str(self.container).find(" ")
                self.end = str(self.container).find(">", self.start + 1)
                self.id = str(self.container)[self.start + 1:self.end]
                self.containers.append(client.containers.get(self.id).attrs['Config']['Image'])
            return max([len(item) for item in self.containers])
        else:
            return 0


    def listImages(self):
        # Create a Dataframe listing all the docker images
        self.stdout = externalCmd("docker images")
        return pd.read_fwf(StringIO(self.stdout), widths=[self.longestImageName(), 20, 20, 20, 20])


    def imageDetails(self, image):
        # Create a Dataframe listing details of a specific docker image
        self.stdout = externalCmd("docker inspect " + image)
        return pd.read_json(self.stdout)


    def instanceDetails(self, container_id):
        # Create a Dataframe listing details of a specific docker instance
        self.stdout = externalCmd("docker inspect " + container_id)
        return pd.read_json(self.stdout)


    def listInstances(self):
        # Create a Dataframe listing all the docker instances
        self.stdout = externalCmd("docker ps")
        return pd.read_fwf(StringIO(self.stdout), widths=[20, self.longestContainerName(), 20, 20, 20, 20, 20])

    def pullImage(self, image):

        try:
            self.stdout = externalCmd("docker pull " + image)
            if "Image is up to date" in self.stdout:
                print("Image was up to date...")
            else:
                print("New image added")
        except:
            pass

    def removeImage(self, image):
        try:
            externalCmd("docker rmi --force " + image)
        except:
            pass

    def pauseInstance(self, container_id):
        try:
            externalCmd("docker pause " + container_id)
        except:
            pass

    def unpauseInstance(self, container_id):
        try:
            externalCmd("docker unpause " + container_id)
        except:
            pass

    def restartInstance(self, container_id):
        try:
            externalCmd("docker restart " + container_id)
        except:
            pass

    # User requested to instantiate an image
    def instantiatelImage(self, image, userpassword):

        # Create the instance.
        if len(glob.launchCommands[image]) > 1:

            self.cmd_create = glob.launchCommands[image][0]
            self.cmd_run = glob.launchCommands[image][1]

            if "<password>" in self.cmd_create:
                self.cmd_create = self.cmd_create.replace("<password>", userpassword)

            if "<port>" in self.cmd_create:
                self.port = getNewPort()
                externalCmdLive(self.cmd_create.replace("<port>", str(self.port)))
                externalCmdLive(self.cmd_run.replace("<port>", str(self.port)))
            else:
                externalCmdLive(self.cmd_create)
                externalCmdLive(self.cmd_run)
        else:
            # stuff to open directly in a terminal
            externalCmdLive(glob.launchCommands[image][1])

    # container already created but closed. User wants to re-open it
    def openInstance(self, container_id):
        # let's see if that container has exposed a port, if so, let's run it
        self.details = dockerAPI.instanceDetails(container_id)["Config"].to_dict()
        try:
            self.port = self.details[0]["8787/tcp"][0]["HostPort"]
            print("port" + self.port)
            #self.port = str(list(self.details[0]["HostConfig"])[0]).split("/")[0]
            print("Re-opening container " + str(container_id) + " on " + self.port)
            externalCmdLive(glob.internerBrowser + " http://127.0.0.1:" + self.port + "/")
        except:
            try:
                self.cmd = str(list(self.details[0]["Cmd"])[0])
                externalCmdLive("konsole -e docker exec -ti "+ container_id + " " + self.cmd)
            except:
                pass


    def stopInstance(self, container_id):
        # send SIGTERM signal, trying a gracefull shutdown. SIGKILL is sent after a grace period.
        try:
            externalCmd("docker stop " + container_id)
        except:
            print("Couldn't stop")