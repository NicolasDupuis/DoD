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
        self.mounts = []

        for self.instance in docker.from_env().containers.list():
            self.instance = str(self.instance)
            self.instance = self.instance.replace("<Container:", "")
            self.instance = self.instance.replace(">", "")

            self.details = dockerAPI.instanceDetails(self.instance).to_dict()

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

                # mounted volumes
                self.mounts.append(self.details["HostConfig"][0]["Binds"])

        self.data = list(zip(self.ids, self.names, self.ports, self.status, self.created, self.images, self.mounts))

        return pd.DataFrame(self.data, columns=['ID', 'Names', 'Ports', 'Status', 'Created', 'Images', 'Mounts'])


    def listVolumes(self):
        # Create a Dataframe listing all the docker volumes
        self.stdout = externalCmd("docker volume ls")
        return pd.read_fwf(StringIO(self.stdout), widths=[20, 64])

    def pullImage(self, image):

        try:
            externalCmd(glob.terminal + "docker pull " + image)
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
    def instantiatelImage(self, image, role, username, userpassword, volume, mountPoint):

        self.cmd_create = glob.launchCommands[image]["create"]

        # placeholder for username
        if "<userid>" in self.cmd_create:
            self.cmd_create = self.cmd_create.replace("<userid>", username)

        # placeholder for container's name
        if "<#n#>" in self.cmd_create:
            self.instances = dockerAPI.listInstances(role=role, username=username)
            self.instances = sorted([instance for instance in list(self.instances["Names"]) if glob.launchCommands[image]["name"] in instance])

            if len(self.instances) == 0:  # no container for this image yet
                self.container_n = "-1"
            else:
                self.container_n = "-" + str(int(self.instances[-1].split("-")[1]) + 1)

            self.cmd_create = self.cmd_create.replace("<#n#>", self.container_n)

        # placeholder for user password
        if "<password>" in self.cmd_create:
            self.cmd_create = self.cmd_create.replace("<password>", userpassword)

        if "<volume>" in self.cmd_create:
            if volume in ["none","default"]:
                self.cmd_create = self.cmd_create.replace("<volume>", "")
            else:
                self.cmd_create = self.cmd_create.replace("<volume>", "-v " + volume + ":" + mountPoint + " ")

        # placeholder for port
        if "<port>" in self.cmd_create:
            self.port = getNewPort()
            self.cmd_create = self.cmd_create.replace("<port>", str(self.port))

        print("Create command: " + str(self.cmd_create))

        # let's create this thing
        externalCmdLive(self.cmd_create)

        # do we need to run it in a browser?
        try:
            self.cmd_run = glob.launchCommands[image]["run"]
            externalCmdLive(self.cmd_run.replace("<port>", str(self.port)))
        except:
            pass


    # container already created but closed. User wants to re-open it
    def openInstance(self, container_id):

        try:
            # let's see if that container has exposed a port, if so, let's run it
            self.port = dockerAPI.instanceDetails(container_id)["HostConfig"].to_dict()[0]["PortBindings"]["8787/tcp"][0]["HostPort"]
            print("Re-opening container " + str(container_id) + " on " + self.port)
            externalCmdLive(glob.internerBrowser + " http://127.0.0.1:" + self.port + "/")
        except:
            try:
                self.dockercmd = dockerAPI.instanceDetails(container_id)["Config"].to_dict()[0]["Cmd"][0]
                self.cmd = "docker exec -ti " + container_id + " " + str(self.dockercmd)
                print("Re-open command: " + str(self.cmd))
                externalCmdLive(glob.terminal + self.cmd)
            except:
                print("Re-open " + str(container_id) + "? Errr, not sure how to do that...")


    def stopInstance(self, container_id):
        # send SIGTERM signal, trying a gracefull shutdown. SIGKILL is sent after a grace period.
        try:
            externalCmd("docker stop " + container_id)
        except:
            print("Couldn't stop")