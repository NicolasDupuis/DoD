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

    def listImages(self):
        # Create a Dataframe listing all the docker images
        self.stdout = externalCmd("docker images")
        return pd.read_fwf(StringIO(self.stdout), widths=[max(20, self.longestImageName()), 20, 20, 20, 20])


    def imageDetails(self, image):
        # Create a Dataframe listing details of a specific docker image
        self.stdout = externalCmd("docker inspect " + image)
        return pd.read_json(self.stdout)


    def instanceDetails(self, container_id):
        # Create a Dataframe listing details of a specific docker instance
        self.stdout = externalCmd("docker inspect " + container_id)
        return pd.read_json(self.stdout)

    def volumeDetails(self, volume_id):
        # Create a Dataframe listing details of a specific docker instance
        self.stdout = externalCmd("docker volume inspect " + volume_id)
        return pd.read_json(self.stdout)

    # Create a Dataframe listing all the docker instances
    def listInstances(self, role, username):

        self.ids = []; self.names = []; self.ports = []; self.status = []; self.created = []; self.images = []

        for self.instance in docker.from_env().containers.list():
            self.instance = str(self.instance)
            self.instance = self.instance.replace("<Container:", "")
            self.instance = self.instance.replace(">", "")

            self.details = dockerAPI.instanceDetails(self.instance).to_dict()

            print("Username: " + str(username))
            print("name: " + str(self.details["Name"][0][1:]))

            # Admins: shows all containers. Users: only show theirs
            if role == glob.roles[1] or username in self.details["Name"][0][1:]:

                # container id
                self.ids.append(self.details["Id"][0])

                # names
                self.names.append(self.details["Name"][0][1:])

                # ports
                try:
                    self.ports.append(self.details["HostConfig"][0]["PortBindings"]["8787/tcp"][0]["HostPort"])
                except:
                    self.ports.append("N/A")

                # status
                self.status.append(self.details["State"][0]["Status"])

                # created
                self.created.append(self.details["Created"][0])

                # image
                self.images.append((self.details["Config"][0]["Image"]))

        self.data = list(zip(self.ids, self.names, self.ports, self.status, self.created, self.images))

        return pd.DataFrame(self.data, columns=['ID', 'Names', 'Ports', 'Status', 'Created', 'Images'])


    def listVolumes(self):
        # Create a Dataframe listing all the docker volumes
        self.stdout = externalCmd("docker volume ls")
        return pd.read_fwf(StringIO(self.stdout), widths=[20, 64])

    def pullImage(self, image):

        try:
            self.stdout = externalCmd("docker pull " + image)
            if "Image is up to date" in self.stdout:
                print("Image was up to date...")
            else:
                print("New image added")
        except:
            pass

    def createVolume(self, volume):
        try:
            self.stdout = externalCmd("docker volume create " + volume)
        except:
            pass

    def removeImage(self, image):
        try:
            externalCmd("docker rmi --force " + image)
        except:
            pass

    def deleteVolume(self, volume_id):
        try:
            externalCmd("docker volume rm " + volume_id)
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
    def instantiatelImage(self, image, username, userpassword):

        # Create the instance.
        if len(glob.launchCommands[image]) > 1:

            self.cmd_create = glob.launchCommands[image][0]
            self.cmd_run = glob.launchCommands[image][1]

            if "<userid>" in self.cmd_create:
                self.cmd_create = self.cmd_create.replace("<userid>", username)

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
            externalCmdLive(glob.launchCommands[image][0])

    # container already created but closed. User wants to re-open it
    def openInstance(self, container_id):

        try:
            # let's see if that container has exposed a port, if so, let's run it
            self.details = dockerAPI.instanceDetails(container_id)["HostConfig"].to_dict()
            self.port = self.details[0]["PortBindings"]["8787/tcp"][0]["HostPort"]
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