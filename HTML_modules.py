 
def header_layout():
    return '''
    <html>
    <title>d-wise on demand</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    
    <style>
    html,body,h1,h2,h3,h4,h5 {font-family: "Raleway", sans-serif}
    </style>
    <body class="w3-light-white">
    '''

def topContainer_Layout():
    return '''<!-- Top container -->
    <div class="w3-bar w3-top w3-blue w3-large" style="z-index:4">
    <span class="w3-bar-item w3-right"><strong>d-wise</strong> on demand</span>
    </div>'''


def sidebar_layout(username, role, current):

    color = ["", "", "", ""]
    if current == "dockerlibrary":
        color[0] = "w3-blue"
    elif current == "dockerInstances":
        color[1] = "w3-blue"
    elif current == "volumeslibrary":
        color[2] = "w3-blue"
    elif current == "usersMgmt":
        color[3] = "w3-blue"

    if role == glob.roles[0]:  # users
        sections = '<a href="dockerlibrary"   class="w3-bar-item w3-button w3-padding ' + color[0] + '"><img src = "./static/hub-icon.png" style="width:25px;border:0;"></img>  Images library</a>'
        sections += '<a href="dockerInstances" class="w3-bar-item w3-button w3-padding ' + color[1] + '"><img src = "./static/docker-icon.png" style="width:32px;border:0;"> </img>  Active containers</a>'

    elif role == glob.roles[1]:  # admin
        sections = '<a href="dockerlibrary"   class="w3-bar-item w3-button w3-padding ' + color[0] + '"><img src = "./static/hub-icon.png" style="width:25px;border:0;"></img>  Images library</a>'
        sections += '<a href="dockerInstances" class="w3-bar-item w3-button w3-padding ' + color[1] + '"><img src = "./static/docker-icon.png" style="width:32px;border:0;"></img>  Active containers</a>'
        sections += '<a href="volumeslibrary" class="w3-bar-item w3-button w3-padding ' + color[2] + '"><img src = "./static/volume.png" style="width:32px;border:0;">Volumes library</a>'

    return '''
    <!-- Sidebar/menu -->
    <nav class="w3-sidebar w3-collapse w3-white w3-animate-left" style="z-index:3;width:300px;" id="mySidebar"><br>
      <div class="w3-container w3-row">
        <div class="w3-col s4">
          <img src="https://www.w3schools.com/w3images/avatar2.png" class="w3-circle w3-margin-right" style="width:46px">
        </div>
        <div class="w3-col s8 w3-bar">
          <span>Welcome, <strong>''' + username + '''</strong></span><br>
          <a href="/index"><img src="/static/sign_out.png" alt="sign_out" style="width:25px;height:25px;border:0;"></a>
        </div>
      </div>
      <hr>
      <div class="w3-container">
        <h5>''' + role + ''' view</h5>
      </div>
      <div class="w3-bar-block">
        <a href="#" class="w3-bar-item w3-button w3-padding-16 w3-hide-large w3-dark-grey w3-hover-black" onclick="w3_close()" title="close menu"><i class="fa fa-remove fa-fw"></i>  Close Menu</a>
        ''' + sections + '''
      </div>
    </nav>

    <!-- Overlay effect when opening sidebar on small screens -->
    <div class="w3-overlay w3-hide-large w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>
    '''

def dockerImages_layout(username, role):
    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;"><br>
      <h2><img src = "./static/hub-icon.png" style="width:50px;border:0;"></img>  Docker images library</h2>
      <br> '''

    # dataframes with Docker hub and user-defines images
    images = dockerAPI.listImages()

    dockerhubs = images[images["AUTHOR"] == "Docker hub"].reset_index().drop(['index'], axis=1)
    userdefined = images[images["AUTHOR"] == username].reset_index().drop(['index'], axis=1)

    # HTML code for docker hub images
    html_code += '''<h4>Docker Hub images</h4><hr>'''
    if len(dockerhubs) > 0:
        for i in range(len(dockerhubs)):
            nickname = glob.images[str(dockerhubs.loc[i][0])]["nickname"]

            html_code += '''
            <td><strong>''' + nickname + '''</strong> (''' + str(dockerhubs.loc[i][0]) + ''')</td>
            <table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white">
            <tr><td> <img src="''' + glob.images[dockerhubs.loc[i][0]]["icon"] + '''" alt="''' + str(dockerhubs.loc[i][0]) + '''" style="width:100px;border:0;"> </td>
                <td> Tag: ''' + str(dockerhubs.loc[i][1]) + '''<br>
                     Created: ''' + str(dockerhubs.loc[i][3]) + ''' <br>
                     Validated: ''' + str(glob.images[str(dockerhubs.loc[i][0])]["validated"]) + ''' </td>
                <td><br> <a href="/imageDetails?image=''' + str(dockerhubs.loc[i][0]) + '''">
                        <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/imageLaunchPad?image=''' + str(dockerhubs.loc[i][0]) + '''&mode=now">
                        <img src="/static/run.jpg" title="Run" alt="Run now" title="Run now" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/imageLaunchPad?image=''' + str(dockerhubs.loc[i][0]) + '''&mode=configure">
                        <img src="/static/run_configure.png" title="Configure and run" alt="Run" title="Configure and run" style="width:42px;height:42px;border:0;">
                     </a>
                     '''
            if role == glob.roles[1]:  # admin
                html_code += ''' <a href="/deleteImage?image=''' + str(dockerhubs.loc[i][0]) + '''">
                                   <img src="/static/delete.jpg" title="Delete" alt="details" style="width:42px;height:42px;border:0;">
                                 </a>  '''
            html_code += "</td></tr>"
            html_code += "</table><br>"
    else:
        html_code += '''<img src="/static/empty_box.jpg" alt="empty box" style="width:200px;border:0;"> '''

    if role == glob.roles[1]:  # admin
        html_code += ''' <br><br>
          <form action ="/pullImage" method = GET>
           Pull an image from Docker Hub:
           <table>
            <tr><td><input name = "image"></td>
            <td><input type=submit class="button" value="Pull!"></td></tr>
           </table >
           </form>
           '''
    # HTML code for user-defined images
    html_code += '''<br><h4>User-defined images</h4><hr>'''
    if len(userdefined) > 0:
        for i in range(len(userdefined)):
            html_code += '''
                <td><strong>''' + glob.images[str(userdefined.loc[i][0])]["nickname"] + '''</strong> (''' + str(userdefined.loc[i][0]) + ''')</td>
                <table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white">
                <tr><td> <img src="''' + glob.images[userdefined.loc[i][0]]["icon"] + '''" alt="''' + str(userdefined.loc[i][0]) + '''" style="width:100px;border:0;"> </td>
                    <td> Tag: ''' + str(userdefined.loc[i][1]) + '''<br>
                         Created: ''' + str(userdefined.loc[i][3]) + ''' <br>
                         Validated: ''' + str(glob.images[str(userdefined.loc[i][0])]["validated"]) + ''' </td>
                    <td><br> <a href="/imageDetails?image=''' + str(userdefined.loc[i][0]) + '''">
                            <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
                         </a>
                         <a href="/imageLaunchPad?image=''' + str(userdefined.loc[i][0]) + '''&mode=now">
                            <img src="/static/run.jpg" title="Run" alt="Run now" title="Run now" style="width:42px;height:42px;border:0;">
                         </a>
                         <a href="/imageLaunchPad?image=''' + str(userdefined.loc[i][0]) + '''&mode=configure">
                            <img src="/static/run_configure.png" title="Configure and run" alt="Run" title="Configure and run" style="width:42px;height:42px;border:0;">
                         </a>
                         <a href="/deleteImage?image=''' + str(userdefined.loc[i][0]) + '''">
                                       <img src="/static/delete.jpg" title="Delete" alt="details" style="width:42px;height:42px;border:0;">
                                     </a></td></tr></table><br>'''
    else:
        html_code += '''<img src="/static/empty_box.jpg" title="No images found" alt="empty box" style="width:200px;border:0;"> '''

    if len(userdefined) + len(dockerhubs) == 0:
        html_code += '''<center><br><img src="/static/empty_box.jpg" alt="empty box"> '''
        html_code += "Sorry, no images available...</center>"

    return html_code


def imageLaunchPad_layout(image):
    html_code = '''<!-- !PAGE CONTENT! -->
          <div class="w3-main" style="margin-left:300px;margin-top:43px;">

            <!-- Header -->
            <header class="w3-container" style="padding-top:22px">
              <h4><b><i class="fa fa-dashboard"></i> Docker image launchpad</b></h4>
            </header> 
            <br> We're about to run <strong>''' + image + ''' </strong> for you. Just a few questions first...<br>            
            '''
    # list available volumes for mounting
    listvolumes = "<option value = image=" + image + "&volume=none>None</option>"
    if glob.images[image]["mountDefault"] == "None":
        listvolumes += "<option value = image=" + image + "&volume=none selected='selected'>None</option>"
    else:
        listvolumes += "<option value = image=" + image + "&volume=none >None</option>"
    volumes = dockerAPI.listVolumes()
    for i in range(len(volumes)):
        if glob.images[image]["mountDefault"] == volumes.loc[i][1]:
            listvolumes += "<option value = image=" + image + "&volume=" + volumes.loc[i][1] + " selected='selected'>" + volumes.loc[i][1] + "</option>"
        else:
            listvolumes += "<option value = image=" + image + "&volume=" + volumes.loc[i][1] + ">" + volumes.loc[i][1] + "</option>"

    html_code += '''<br><form action ="/actionsImage?run_''' + image + '''" method = GET> '''
    html_code += '''<table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white"> '''
    html_code += "    <tr><td>Persistent storage</td>"
    html_code += '''      <td>Do you need to mount a volume in your container? <br>
                          <select name = "run" size = "4" single ''' + listvolumes + '''</select>
                          <br>Where should we mount this volume? 
                          <input name = "mountPoint" value= ''' + glob.images[image]["mountPoint"] + '''>
                          <br>
                          <input type="checkbox" name="remember" value="True"> Remember my choice and make it my default<br>
                          </td></tr>
                      <tr><td>Performance</td>
                          <td>Leave blank for default.<br>How many CPU: <input name = "cpu"> 
                          <br>Max memory (MB): <input name = "ram"></td></tr>
                     </table><br><input type=submit class="button" value="Launch !"> 
                    </form>'''

    return html_code

def dockerImagesDetails_layout(role, image):

    if role == glob.roles[1]:  # admin
        disabled = ""
    else:
        disabled = " disabled"

    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">
      <table style="width:60%" class="w3-table w3-striped w3-white">
        <tr><td><h3>Details for image "''' + image + '''"</h3></td>
                 <td><img src="''' + glob.images[image]["icon"] + '''" alt=Logo align="right" width="100"></td></tr></table>
        <br><h4>App settings</h4><hr>
        <form action ="/imageSettings" method=GET>
        <table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white">
        <tr><td>Image name</td><td><input name = "image" value =''' + image + ''' ''' + disabled + ''' ></td></tr>'''

    for item in list(glob.images[image].keys()):
        html_code += '''<tr><td>''' + item + '''</td>
                       <td><input name = "''' + item + '''" value="''' + str(glob.images[image][item]) + '''"''' + disabled + '''
                        </td></tr>'''

    html_code +=''' </table><br><input type = submit class = "button" value = "Update" ''' + disabled + '''></form>
                    <br><h4>Docker low-level details</h4><hr>
                    <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
                    <tr><th>Item</th><th>Value</th></tr><tr> '''

    details = dockerAPI.imageDetails(image)  # get a dataframe
    for i in range(len(details.columns)):
        _items = ""
        if isinstance(details.loc[0][i], dict):
            for item in details.loc[0][i]:
                _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
        else:
            _items = str(details.loc[0][i])

        html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
        html_code += "    <td>" + _items + "</td></tr>"

    html_code += "</table></div>"

    return html_code

def imageClone_layout(image, container_name, container_id):

    html_code = '''<!-- !PAGE CONTENT! -->
          <div class="w3-main" style="margin-left:300px;margin-top:43px;">

            <!-- Header -->
            <header class="w3-container" style="padding-top:22px">
              <h4><b><i class="fa fa-dashboard"></i> Docker image cloning factory</b></h4>
            </header> 
            <br> We're about to clone the current state of <strong>''' + container_name + ''' </strong> for you. Just a few questions first...<br>            
            '''
    html_code += '''<br><form action ="/cloneImage" method = GET> '''
    html_code += '''<table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white"> '''
    html_code += '''<tr><td>Parent image: </td><td><input name = "old_image" value = ''' + image + '''></td></tr> 
                    <tr><td>Container ID: </td><td><input name = "container_id" value = ''' + container_id + '''></td></tr> 
                     <tr><td>New image name: </td><td><input name = "new_image"></td></tr>
                     <tr><td>New image tag: </td><td><input name = "tag" value="Latest"></td></tr>     
                     </table><br><input type=submit class="button" value="Clone !"> 
                    </form>'''
    return html_code


##########################################################################################################################################
# Layouts for Docker Instances
##########################################################################################################################################


def dockerInstances_layout(username, role):

    # find all the active docker instances for that user, get a dataframe with high level details
    instances = dockerAPI.listInstances(role=role, username=username)

    # build HTML code
    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;"><br>
      <h2><img src = "./static/docker-icon.png" style="width:50px;border:0;"></img>  Your active Docker containers</h2>
      <br> '''

    if len(instances) > 0:

        for i in range(len(instances)):

            container_id = str(instances.loc[i][0][:12])
            image = str(instances.loc[i][5])

            volume = str(instances.loc[i][6]).split(":")[0]
            if volume != "None":
                volume = str(instances.loc[i][6]).split(":")[1][:-2]

            html_code += '''<br><td><strong>''' + str(instances.loc[i][1]) + '''</strong></td>
            <table style="width:80%" class="w3-table w3-striped w3-bordered w3-border w3-white">
            <tr><td> <img src="''' + glob.images[image]["icon"] + '''" alt="''' + str(instances.loc[i][5]) + '''" style="width:100px;border:0;"> </td>
                <td> Container ID: ''' + container_id + '''<br>
                     Image: ''' + image + '''<br> 
                     Created: ''' + str(instances.loc[i][4]).split(".")[0].replace("T", " at ") + '''<br>
                     Status: ''' + str(instances.loc[i][3]) + '''<br>
                     Port: ''' + str(instances.loc[i][2]) + '''<br>
                     Storage: ''' + volume + '''<br></td>
                
                <td> <br><a href="/actionsInstance?open=''' + container_id + '''">
                        <img src="/static/open.png" title = "Open" alt="open" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?stop=''' + container_id + '''">
                        <img src="/static/stop.jpg" title = "Stop" alt="stop" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?pause=''' + container_id + '''">
                        <img src="/static/pause.png" title = "Pause" alt="pause" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?unpause=''' + container_id + '''">
                        <img src="/static/unpause.jpg" title = "Unpause" alt="unpause" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?restart=''' + container_id + '''">
                        <img src="/static/restart.jpg" title = "Restart" alt="restart" style="width:42px;height:42px;border:0;">
                     </a>                     
                     <a href="/instanceDetails?container_id=''' + container_id + '''">
                        <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
                     </a> 
                    <a href="/cloneImageinfo?image=''' + image + '''&container_name=''' + str(instances.loc[i][1]) + '''&container_id= ''' + str(instances.loc[i][0][:12]) + '''">
                       <img src="/static/clone.png" title="Clone" alt="Clone" style="width:42px;height:42px;border:0;">
                    </a>
                    </td></tr> </table></form>'''

    else:
        html_code += '''<center><br><br><br><img src="/static/empty_box.jpg" alt="empty box"> '''
        html_code += "Sorry, no docker instances available...</center>"

    return html_code


def instanceDetails_layout(container_id):
    html_code += ''' 
      Details for instance <strong>''' + container_id + ''' </strong>:
      <div class="w3-container">
       <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
      <tr>
     <th>Item</th>
     <th>Value</th>                
     </tr><tr> '''

    details = dockerAPI.instanceDetails(container_id)  # get a dataframe

    for i in range(len(details.columns)):
        _items = ""
        if isinstance(details.loc[0][i], dict):
            for item in details.loc[0][i]:
                _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
        else:
            _items = str(details.loc[0][i])

        html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
        html_code += "    <td>" + _items + "</td></tr>"

    return html_code


def dockerInstanceDetails_layout(container_id):
    html_code = '''<!-- !PAGE CONTENT! -->
          <div class="w3-main" style="margin-left:300px;margin-top:43px;">

            <!-- Header -->
            <header class="w3-container" style="padding-top:22px">
              <h2>Details for active container "''' + container_id + '''"</h2>
            </header>
            <div class="w3-container">
               <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
                <tr><th>Item</th><th>Value</th></tr><tr> '''

    details = dockerAPI.instanceDetails(container_id)  # get a dataframe
    for i in range(len(details.columns)):
        _items = ""
        if isinstance(details.loc[0][i], dict):
            for item in details.loc[0][i]:
                _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
        else:
            _items = str(details.loc[0][i])

        html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
        html_code += "    <td>" + _items + "</td></tr>"

    return html_code

##########################################################################################################################################
# Layouts for Docker Volumes
##########################################################################################################################################


def dockerVolumes_layout():

    # fnd all the active docker instances, get a dataframe with high level details
    volumes = dockerAPI.listVolumes()

    # build HTML code
    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;"><br>
      <h2><img src = "./static/volume.png" style="width:50px;border:0;"></img>  Docker volumes</h2>
      <br> '''

    if len(volumes) > 0:
        html_code += '''
      <div class="w3-container">
      <form action="/actionsVolume">
        <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
        <tr><th>DRIVER</th>
            <th>VOLUME NAME</th>            
        </tr>'''
        for i in range(len(volumes)):
            html_code += "<tr><td>" + str(volumes.loc[i][0]) + "</td>"
            html_code += "    <td>" + str(volumes.loc[i][1]) + "</td>"
            html_code += '''  <td> 
              <a href="/actionsVolume?action=details&volume=''' + str(volumes.loc[i][1])  + '''">
                <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
              </a>   
              <a href="/actionsVolume?action=delete&volume=''' + str(volumes.loc[i][1]) + '''">
                <img src="/static/delete.jpg" title="Delete" alt="details" style="width:42px;height:42px;border:0;">
              </a></td></tr> '''

        html_code += "</table></form><br>"
    else:
        html_code += '''<center><br><br><br><img src="/static/empty_box.jpg" alt="empty box"> '''
        html_code += "Sorry, no volumes available...</center>"

    html_code += '''
     <br><hr><form action ="/createVolume" method = GET>
       <h3>Create a new volume</h3>
       <table>
        <tr><td>Volume name</td><td><input name = "volume"></td></tr>
        <tr><td>Root password</td><td><input name="root_password" type="password" placeholder="Enter the root password"/</td></tr>
        </table ><br>
        <input type=submit class="button" value="Create!"></td></tr>
       </form>'''

    return html_code


def volumeDetails_layout(volume):
    # build HTML code
    html_code = '''
        <!-- !PAGE CONTENT! -->
        <div class="w3-main" style="margin-left:300px;margin-top:43px;">
        <!-- Header -->
        <header class="w3-container" style="padding-top:22px">
         <h4> Details for Docker volume <strong>''' + volume + '''</strong></h4>
        </header>
        <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
        <tr>
        <th>Item</th>
        <th>Value</th>                
        </tr>'''

    details = dockerAPI.volumeDetails(volume)  # get a dataframe

    for i in range(len(details.columns)):
        _items = ""
        if isinstance(details.loc[0][i], dict):
            for item in details.loc[0][i]:
                _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
        else:
            _items = str(details.loc[0][i])

        html_code += '''<tr><td>''' + str(list(details.columns)[i]) + '''</td>
                        <td> ''' + _items + '''</td></tr>'''

    html_code += "</table>"

    return html_code


def footer_layout():
    return '''
    <!-- End page content -->
    </div>

    <script>
    // Get the Sidebar
    var mySidebar = document.getElementById("mySidebar");

    // Get the DIV with overlay effect
    var overlayBg = document.getElementById("myOverlay");

    // Toggle between showing and hiding the sidebar, and add overlay effect
    function w3_open() {
        if (mySidebar.style.display === 'block') {
            mySidebar.style.display = 'none';
            overlayBg.style.display = "none";
        } else {
            mySidebar.style.display = 'block';
            overlayBg.style.display = "block";
        }
    }

    // Close the sidebar with the close button
    function w3_close() {
        mySidebar.style.display = "none";
        overlayBg.style.display = "none";
    }
    </script>

    </body>
    </html>'''