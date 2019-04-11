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
        # get image ID (for both hub's and cloned images)
        self.images = dockerAPI.listImages()
        self.image_id = list(self.images[self.images["REPOSITORY"] == image]["IMAGE ID"])[0]

        # Create a Dataframe listing details of a specific docker image
        self.stdout = externalCmd("docker inspect " + self.image_id)
        return pd.read_json(self.stdout)

    def instanceDetails(self, container_id):
        # Create a Dataframe listing details of a specific docker instance
        self.stdout = externalCmd("docker inspect " + container_id)
        return pd.read_json(self.stdout)

    def volumeDetails(self, volume):
        # Create a Dataframe listing details of a specific docker instance
        self.stdout = externalCmd("docker volume inspect " + volume)
        return pd.read_json(self.stdout)

    # Create a Dataframe listing all the docker instances
    def listInstances(self, role=None, username=None):

        self.ids = []; self.names = []; self.ports = []; self.status = []; self.created = []; self.imagestoappend = []
        self.mounts = []

        for self.instance in docker.from_env().containers.list():
            self.instance = str(self.instance)
            self.instance = self.instance.replace("<Container:", "")
            self.instance = self.instance.replace(">", "")

            self.details = dockerAPI.instanceDetails(self.instance).to_dict()

            # Admins: shows all containers. Users: only show theirs. If no info, show all
            if not(role) or (role == glob.roles[1] or username in self.details["Name"][0][1:]):

                # container id
                self.ids.append(self.details["Id"][0])

                # names
                self.names.append(self.details["Name"][0][1:])

                # image
                self.image_id = self.details["Config"][0]["Image"]
                self.allimages = self.listImages()
                self.image = list(self.allimages[self.allimages["IMAGE ID"] == self.image_id]["REPOSITORY"])[0]
                self.imagestoappend.append(self.image)

                # ports
                if glob.images[self.image]["exposedPort"] in ["True", True]:
                    self.exposedPort = str(glob.images[self.image]["exposedPort"])
                    self.ports.append(self.details["HostConfig"][0]["PortBindings"][self.exposedPort + "/tcp"][0]["HostPort"])
                else:
                    self.ports.append("N/A")

                # status
                self.status.append(self.details["State"][0]["Status"])

                # created
                self.created.append(self.details["Created"][0])

                # mounted volumes
                self.mounts.append(self.details["HostConfig"][0]["Binds"])

        self.data = list(zip(self.ids, self.names, self.ports, self.status, self.created, self.imagestoappend, self.mounts))

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

    def createVolume(self, volume, root_password):
        self.stdout = externalCmd("docker volume create " + volume)
        mountpoint = self.volumeDetails(volume).loc[0]["Mountpoint"]
        os.system('echo %s|sudo -S %s' % (root_password, "chmod 775 " + mountpoint))
        os.system('echo %s|sudo -S %s' % (root_password, "chgrp 1000 " + mountpoint))

    def removeImage(self, image):
        # get image ID (for both hub's and cloned images)
        self.images = dockerAPI.listImages()
        self.image_id = self.images[self.images["REPOSITORY"] == image].loc[0]["IMAGE ID"]

        try:
            externalCmd("docker rmi --force " + image_id)
        except:
            pass

    def deleteVolume(self, volume):
        try:
            externalCmd("docker volume rm " + volume)
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

    def commitContainer(self, old_image, container_id, new_image, tag):

        # commit the container changes to a new image
        externalCmd("docker commit " + container_id + " " + new_image + ":" + tag)

        # inherit image properties
        glob.images[new_image] = glob.images[old_image]

        # save to json
        with open('images.json', 'w') as fp:
            json.dump(glob.images, fp)


    # Instantiate an image
    def instantiatelImage(self, image, role, username, userpassword, volume=None, mountPoint=None, cpu=None, ram=None):

        # get image ID (for both hub's and cloned images)
        self.images = dockerAPI.listImages()

        if glob.images[image]["webapp"] in ["True", True]:
            print("Webapp")
            self.cmd_create = "docker run --name <userid>_<nickname><#n#>--rm <volume>-dp <port><password><CPU><RAM><user><GID><image>"
        else:
            print("Terminal")
            self.cmd_create = glob.terminal + "docker run --name <userid>_<nickname><#n#><volume>-ti --rm <image>"

        # placeholder for container's future name: 3 parts (user ID, image nickname, increment integer)
        # 1) user ID
        self.cmd_create = self.cmd_create.replace("<userid>", username)

        # 2) image nickname
        self.cmd_create = self.cmd_create.replace("<nickname>", glob.images[image]["nickname"])

        # 3) increment
        self.instances = dockerAPI.listInstances(role=role, username=username)
        self.instances = sorted([instance for instance in list(self.instances["Names"]) if glob.images[image]["nickname"] in instance])
        if len(self.instances) == 0:  # no container for this image yet
            self.container_n = "-1 "
        else:
            self.container_n = "-" + str(int(self.instances[-1].split("-")[1]) + 1) + " "
        self.cmd_create = self.cmd_create.replace("<#n#>", self.container_n)

        # placeholder for user password
        if glob.images[image]["password"]:
            self.cmd_create = self.cmd_create.replace("<password>", "-e PASSWORD=" + userpassword + " ")
        else:
            self.cmd_create = self.cmd_create.replace("<password>", "")

        # placeholder for volume to mount
        if volume:
            if volume == "None":
                self.cmd_create = self.cmd_create.replace("<volume>", "")
            else:
                self.cmd_create = self.cmd_create.replace("<volume>", "-v " + volume + ":" + mountPoint + volume + " ")
        else:
            self.cmd_create = self.cmd_create.replace("<volume>", "")

        # placeholder for container defined port
        if glob.images[image]["exposedPort"]:
            self.port = getNewPort()
            self.cmd_create = self.cmd_create.replace("<port>", str(self.port)+":"+str(glob.images[image]["exposedPort"]) + " ")
        else:
            self.cmd_create = self.cmd_create.replace("<port>", "")

        # placeholder for CPU and RAM
        if cpu:
            self.cmd_create = self.cmd_create.replace("<CPU>", f'--cpus {cpu} ')
        else:
            self.cmd_create = self.cmd_create.replace("<CPU>", "")

        if ram:
            self.cmd_create = self.cmd_create.replace("<RAM>", f'--memory {ram}m ')
        else:
            self.cmd_create = self.cmd_create.replace("<RAM>", "")

        # use a different GID
        try:
            if glob.images[image]["forceGID"]:
                self.cmd_create = self.cmd_create.replace("<GID>", "-e NB_GID=" + glob.images[image]["forceGID"] + " ")
        except:
            self.cmd_create = self.cmd_create.replace("<GID>", "")

        try:
            if glob.images[image]["user"]:
                self.cmd_create = self.cmd_create.replace("<user>", "--user " + glob.images[image]["user"] + " ")
        except:
            self.cmd_create = self.cmd_create.replace("<user>", "")

        # add stuff
        try:
            if glob.images[image]["postadd"]:
                self.cmd_create += " " + glob.images[image]["postadd"]
        except:
            pass

        self.images = dockerAPI.listImages()
        self.image_id = list(self.images[self.images["REPOSITORY"] == image]["IMAGE ID"])[0]
        print("IMAGE_ID#2 " + str(self.image_id))

        # placeholder for image name
        self.cmd_create = self.cmd_create.replace("<image>", self.image_id)

        # let's create this thing
        print("[NOTE]: Create command: " + str(self.cmd_create))
        externalCmdLive(self.cmd_create)

        # do we need to run it in a browser?
        if glob.images[image]["webapp"]:
            self.cmd_run = glob.internerBrowser + " http://127.0.0.1:" + str(self.port)

            if glob.images[image]["nickname"] == "Jupyter":  # ugly hardcode
                self.cmd_run += "?token=abcdef12345"

            print("[NOTE]: Run command: " + str(self.cmd_run))
            time.sleep(2)
            externalCmdLive(self.cmd_run)


    # container already created but closed. User wants to re-open it
    def openInstance(self, container_id):

        # let's find the image name corresponding to that container ID
        self.image_id = dockerAPI.instanceDetails(container_id)["Config"][0]["Image"]
        self.images = dockerAPI.listImages()
        self.image = list(self.images[self.images["IMAGE ID"] == self.image_id]["REPOSITORY"])[0]
        self.exposedPort = str(glob.images[self.image]["exposedPort"])

        if glob.images[self.image]["webapp"] in ["True", True]:
            self.port = dockerAPI.instanceDetails(container_id)["HostConfig"].to_dict()[0]["PortBindings"]
            self.port = self.port[self.exposedPort + "/tcp"][0]["HostPort"]
            print("Re-opening container " + str(container_id) + " on " + self.port)
            externalCmdLive(glob.internerBrowser + " http://127.0.0.1:" + self.port + "/")
        else:
            self.dockercmd = dockerAPI.instanceDetails(container_id)["Config"].to_dict()[0]["Cmd"][0]
            self.cmd = "docker exec -ti " + container_id + " " + str(self.dockercmd)
            print("Re-open command: " + str(self.cmd))
            externalCmdLive(glob.terminal + self.cmd)

    PortBindings: {'8787/tcp': [{'HostIp': '', 'HostPort': '8501'}]}
    PortBindings: {'8888/tcp': [{'HostIp': '', 'HostPort': '8500'}]}


    def stopInstance(self, container_id):
        try:
            # ask politely
            externalCmd("docker stop " + container_id)
            try:
                # then stop asking...
                externalCmd("docker rm " + container_id)
            except:
                pass
        except:
            pass