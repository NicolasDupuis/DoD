 
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
    <body class="w3-light-grey">
    '''

def topContainer_Layout():
    return '''<!-- Top container -->
    <div class="w3-bar w3-top w3-black w3-large" style="z-index:4">
    <button class="w3-bar-item w3-button w3-hide-large w3-hover-none w3-hover-text-light-grey" onclick="w3_open();"><i class="fa fa-bars"></i>  Menu</button>
    <span class="w3-bar-item w3-right"><strong>d-wise</strong> on demand</span>
    </div>'''


def sidebar_layout(username, role, current):

    color = ["", "", "", ""]
    if current == "dockerlibrary":
        color[0] = "w3-blue"
    elif current == "dockerInstances":
        color[1] = "w3-blue"
    elif current == "usersMgmt":
        color[2] = "w3-blue"

    if role == glob.roles[0]:  # users
        sections = '<a href="dockerlibrary"   class="w3-bar-item w3-button w3-padding ' + color[0] + '"><i class="fa fa-eye fa-fw">   </i>  Images library</a>'
        sections += '<a href="dockerInstances"         class="w3-bar-item w3-button w3-padding ' + color[1] + '"><i class="fa fa-users fa-fw"> </i>  Active containers</a>'

    elif role == glob.roles[1]:  # admin
        sections = '<a href="dockerlibrary" class="w3-bar-item w3-button w3-padding ' + color[0] + '"><i class="fa fa-eye fa-fw">   </i>  Images library</a>'
        sections += '<a href="dockerInstances" class="w3-bar-item w3-button w3-padding ' + color[1] + '"><i class="fa fa-users fa-fw"> </i>  Active containers</a>'
        sections += '<a href="usersMgmt" class="w3-bar-item w3-button w3-padding    ' + color[2] + '"><i class="fa fa-eye fa-fw"></i>  Users management</a>'

    return '''
    <!-- Sidebar/menu -->
    <nav class="w3-sidebar w3-collapse w3-white w3-animate-left" style="z-index:3;width:300px;" id="mySidebar"><br>
      <div class="w3-container w3-row">
        <div class="w3-col s4">
          <img src="https://www.w3schools.com/w3images/avatar2.png" class="w3-circle w3-margin-right" style="width:46px">
        </div>
        <div class="w3-col s8 w3-bar">
          <span>Welcome, <strong>''' + username + '''</strong></span><br>
          <a href="/index" class="w3-bar-item w3-button"><i class="fa fa-cog"></i></a>
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

def dockerImages_layout(username, role, image=None):

    html_code = '''<!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">
    
        <!-- Header -->
        <header class="w3-container" style="padding-top:22px">
          <h5><b><i class="fa fa-dashboard"></i> Docker images library</b></h5>
        </header> '''

    images = dockerAPI.listImages()  # Dataframe with details on local docker images
    if len(images) > 0:

        html_code += ''' <div class="w3-container">
          <form action="/actionsImage">
          <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
          <tr>
            <th>Name</th>
            <th>Tag</th>
            <th>ID</th>
            <th>Created</th>
            <th>Size</th>        
          </tr><tr>'''

        for i in range(len(images)):
            html_code += "<tr><td>" + str(images.loc[i][0]) + "</td>"
            html_code += "    <td>" + str(images.loc[i][1]) + "</td>"
            html_code += "    <td>" + str(images.loc[i][2]) + "</td>"
            html_code += "    <td>" + str(images.loc[i][3]) + "</td>"
            html_code += "    <td>" + str(images.loc[i][4]) + "</td>"
            html_code += '''  <td> <input type="submit" name = "details_''' + str(images.loc[i][0]) + '''" value="Details">  '''
            html_code += '''       <input type="submit" name = "run_'''     + str(images.loc[i][0]) + '''" value="Run">  '''
            if role == glob.roles[1]:  # admin
                html_code += '''       <input type="submit" name = "delete_'''  + str(images.loc[i][0]) + '''" value="Delete">  '''
            html_code += "</td></tr>"

        html_code += "</table></form><br>"

        if role == glob.roles[1]:  # admin
            html_code += '''
             <form action ="/actionsImage" method = GET>
               Pull an image from Docker Hub:
               <table>
                <tr><td><input name = "pull_na"></td>
                <td><input type=submit class="button" value="Pull!"></td></tr>
               </table >
               </form>
               '''

        # if a specific image was selected to display its details, then let's get those
        if image != None:
            html_code += ''' 
              Details for image <strong>''' + image + ''' </strong>:
              <div class="w3-container">
                <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
                <tr><th>Item</th><th>Value</th></tr><tr> '''

            details = dockerAPI.imageDetails(image)  # get a dataframe
            for i in range(len(details.columns)):
                _items = ""
                if isinstance(details.loc[0][i], dict):
                    for item in details.loc[0][i] :
                        _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
                else:
                    _items = str(details.loc[0][i])

                html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
                html_code += "    <td>" + _items + "</td></tr>"

    else:
        html_code += "There are no docker images available at this point."

    return html_code


def dockerInstances_layout(username, role, container_id=None):
    # fnd all the active docker instances, get a dataframe with high level details
    instances = dockerAPI.listInstances()

    # build HTML code
    html_code = '''
      <!-- !PAGE CONTENT! -->
      <div class="w3-main" style="margin-left:300px;margin-top:43px;">
      <!-- Header -->
      <header class="w3-container" style="padding-top:22px">
       <h5><b><i class="fa fa-dashboard"></i> Active Docker instances</b></h5>
      </header>
      '''

    if len(instances) > 0:
        html_code += '''
      <div class="w3-container">
      <form action="/actionsInstance">
        <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white">
        <tr><th>CONTAINER ID</th>
            <th>IMAGE</th>
            <th>CREATED</th>
            <th>STATUS</th>
            <th>PORTS</th>        
            <th>NAMES</th>
            <th>ACTIONS</th>
        </tr>'''
        for i in range(len(instances)):
            html_code += "<tr><td>" + str(instances.loc[i][0]) + "</td>"
            html_code += "    <td>" + str(instances.loc[i][1]) + "</td>"
            html_code += "    <td>" + str(instances.loc[i][3]) + "</td>"
            html_code += "    <td>" + str(instances.loc[i][4]) + "</td>"
            html_code += "    <td>" + str(instances.loc[i][5]) + "</td>"
            html_code += "    <td>" + str(instances.loc[i][6]) + "</td>"
            html_code += '''  <td> <input type="submit" name = "open_''' + str(instances.loc[i][0]) + '''" value="Open">  '''
            html_code += '''       <input type="submit" name = "stop_'''    + str(instances.loc[i][0]) + '''" value="Stop">  '''
            html_code += '''       <input type="submit" name = "pause_'''   + str(instances.loc[i][0]) + '''" value="Pause">  '''
            html_code += '''       <input type="submit" name = "unpause_''' + str(instances.loc[i][0]) + '''" value="Unpause">  '''
            html_code += '''       <input type="submit" name = "restart_''' + str(instances.loc[i][0]) + '''" value="Restart">  '''
            html_code += '''       <input type="submit" name = "details_''' + str(instances.loc[i][0]) + '''" value="Details">  '''
            html_code += "</td></tr>"

        html_code += "</table></form><br>"

        if container_id != None:

            html_code += ''' 
              Details for instance <strong>''' + container_id  + ''' </strong>:
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
                    for item in details.loc[0][i] :
                        _items += item + ": " + str(details.loc[0][i][item]) + "<br>"
                else:
                    _items = str(details.loc[0][i])

                html_code += "<tr><td>" + str(list(details.columns)[i]) + "</td>"
                html_code += "    <td>" + _items + "</td></tr>"

    else:
        html_code += "There are no docker instances available at this point."

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
