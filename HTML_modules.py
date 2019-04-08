 
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
        sections += '<a href="dockerInstances" class="w3-bar-item w3-button w3-padding ' + color[1] + '"><img src = "./static/docker-icon.png" style="width:32px;border:0;"> </img>  Active containers</a>'
        sections += '<a href="volumeslibrary" class="w3-bar-item w3-button w3-padding ' + color[2] + '"><i class="fa fa-users fa-fw"> </i>  Volumes library</a>'
        sections += '<a href="usersMgmt" class="w3-bar-item w3-button w3-padding    ' + color[3] + '"><i class="fa fa-eye fa-fw"></i>  Users management</a>'

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
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">

        <!-- Header -->
        <header class="w3-container" style="padding-top:22px">
          <h4><b><img src = "./static/hub-icon.png" style="width:25px;border:0;"></img> Docker images library</b></h4>
        </header> '''

    images = dockerAPI.listImages()  # Dataframe with details on local docker images
    if len(images) > 0:

        html_code += ''' <br>Here is the list of the ''' + str(len(images)) + ''' docker local image(s) you can instantiate: <br>'''

        for i in range(len(images)):
            html_code += '''
            <br><td><strong>''' + glob.images[str(images.loc[i][0])]["nickname"] + '''</strong></td>
            <table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white">
            <tr><td> <img src="/static/''' + str(images.loc[i][0].replace("/","_")) + '''.jpg" alt="''' + str(images.loc[i][0]) + '''" style="width:100px;border:0;"> </td>
                <td> Tag: ''' + str(images.loc[i][1]) + '''<br>
                     Size: ''' + str(images.loc[i][3]) + '''<br>
                     Created: ''' + str(images.loc[i][4]) + ''' </td>
                <td> <a href="/imageDetails?image=''' + str(images.loc[i][0]) + '''">
                        <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/imageLaunchPad?image=''' + str(images.loc[i][0]) + '''">
                        <img src="/static/run.jpg" title="Run" alt="run" style="width:42px;height:42px;border:0;">
                     </a>'''
                
            if role == glob.roles[1]:  # admin
                html_code += '''<a href="/deleteImage?image=''' + str(images.loc[i][0]) + '''">
                                   <img src="/static/delete.jpg" title="Delete" alt="details" style="width:42px;height:42px;border:0;">
                                 </a>  '''

            html_code += "</td></tr>"
            html_code += "</table>"

    else:
        html_code += "There are no docker images available at this point."

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
    volumes = dockerAPI.listVolumes()
    listvolumes = "<option value = image=" + image + "&volume=none> None </option>"
    listvolumes += "<option value = image=" + image + "&volume=default> Default </option>"
    for i in range(len(volumes)):
        listvolumes += "<option value = image=" + image + "&volume=" + volumes.loc[i][1] + ">" + volumes.loc[i][1] + "</option>"
    html_code += '''<br><form action ="/actionsImage?run_''' + image + '''" method = GET> '''
    html_code += '''<table style="width:60%" class="w3-table w3-striped w3-bordered w3-border w3-white"> '''
    html_code += "    <tr><td>Persistent storage</td>"
    html_code += '''      <td>Do you need to mount a volume in your container? <br>
                          <select name = "run" size = "4" single selected=image=" + image + "&volume=none> ''' + listvolumes + '''</select>
                          <br>Where should we mount this volume? 
                          <input name = "mountPoint" value= ''' + glob.images[image]["mountPoint"] + '''></td></tr>
                      <tr><td>Performance</td>
                          <td>Leave blank for default.<br>How many CPU: <input name = "cpu" value= 1> 
                          <br>how much memory (MB): <input name = "ram" value= 16></td></tr>
                     </table><br><input type=submit class="button" value="Launch !"> 
                    </form>'''

    return html_code

def dockerImagesDetails_layout(image):
    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">

        <!-- Header -->
        <header class="w3-container" style="padding-top:22px">
          <h4><b><i class="fa fa-dashboard"></i> Details for image "''' + image  + '''"</b></h4>
        </header>
        <div class="w3-container">
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

    return html_code


def dockerInstances_layout(username, role, container_id=None):

    # find all the active docker instances for that user, get a dataframe with high level details
    instances = dockerAPI.listInstances(role=role, username=username)

    # build HTML code
    html_code = '''
      <!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">
      <!-- Header -->
      <header class="w3-container" style="padding-top:22px">
       <h4><b><img src = "./static/docker-icon.png" style="width:32px;border:0;"> </img> Your active Docker containers</b></h4>
      </header>
      '''

    if len(instances) > 0:
        html_code += '''<div class="w3-container">'''

        for i in range(len(instances)):
            html_code += '''
            
            <br><td><strong>''' + str(instances.loc[i][1]) + '''</strong></td>
            <table style="width:70%" class="w3-table w3-striped w3-bordered w3-border w3-white">
            <tr><td> <img src="/static/''' + str(instances.loc[i][5].replace("/","_")) + '''.jpg" alt="''' + str(instances.loc[i][5]) + '''" style="width:100px;border:0;"> </td>
                <td> ID: ''' + str(instances.loc[i][0][:12]) + '''<br>
                     Image: ''' + str(instances.loc[i][5]) + '''<br> 
                     Created: ''' + str(instances.loc[i][4]) + '''<br>
                     Status: ''' + str(instances.loc[i][3]) + '''<br>
                     Port: ''' + str(instances.loc[i][2]) + '''<br>
                     Mount: ''' + str(instances.loc[i][6]) + '''<br></td>
                
                <td> <a href="/actionsInstance?open=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/open.png" title = "Open" alt="open" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?stop=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/stop.jpg" title = "Stop" alt="stop" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?pause=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/pause.png" title = "Pause" alt="pause" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?unpause=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/unpause.jpg" title = "Unpause" alt="unpause" style="width:42px;height:42px;border:0;">
                     </a>
                     <a href="/actionsInstance?restart=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/restart.jpg" title = "Restart" alt="restart" style="width:42px;height:42px;border:0;">
                     </a>                     
                     <a href="/instanceDetails?container_id=''' + str(instances.loc[i][0]) + '''">
                        <img src="/static/details.jpg" title = "Details" alt="details" style="width:42px;height:42px;border:0;">
                     </a>   
                </td></tr>                
            </table></form><br> '''

    else:
        html_code += "There are no docker instances available at this point."

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
              <h4><b><i class="fa fa-dashboard"></i> Details for active container "''' + container_id + '''"</b></h4>
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


def dockerVolumes_layout(username, role, volume_id=None):

    # fnd all the active docker instances, get a dataframe with high level details
    volumes = dockerAPI.listVolumes()

    # build HTML code
    html_code = '''
      <!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">
      <!-- Header -->
      <header class="w3-container" style="padding-top:22px">
       <h5><b><i class="fa fa-dashboard"></i> Docker volumes</b></h5>
      </header>
      '''

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
            html_code += '''  <td> <input type="submit" name = "details@''' + str(volumes.loc[i][1]) + '''" value="Details">  '''
            html_code += '''       <input type="submit" name = "delete@''' + str(volumes.loc[i][1]) + '''" value="Delete">  '''
            html_code += "</td></tr>"

        html_code += "</table></form><br>"

        if volume_id != None:

            html_code += ''' 
              Details for volume <strong>''' + volume_id  + ''' </strong>:
              <div class="w3-container">
               <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
              <tr>
             <th>Item</th>
             <th>Value</th>                
             </tr><tr> '''

            details = dockerAPI.volumeDetails(volume_id)  # get a dataframe
            for i in range(len(details.columns)):
                _items = ""
                if isinstance(details.loc[0][i], dict):
                    for item in details.loc[0][i] :
                        _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
                else:
                    _items = str(details.loc[0][i])

                html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
                html_code += "    <td>" + _items + "</td></tr>"

    html_code += '''
     <form action ="/actionsVolume" method = GET>
       Create a new volume, please enter a name:
       <table>
        <tr><td><input name = "create@na"></td>
        <td><input type=submit class="button" value="Create!"></td></tr>
       </table >
       </form>'''

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
