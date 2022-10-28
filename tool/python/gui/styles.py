APPBG = "rgb(37, 37, 37)"


appStyles = """
#iGPMT {
    background-color: """+APPBG+""";
}

Heading {
    font-weight: bold;
}

#warning {
    color:red;
    font-weight:bold;
}

Text, QLabel, Heading, QListView, #operationsCont {
    color:white;
    font-size: 16px;
}

Container{
    background-color:rgb(40, 40, 40);
}

ContainerFrame, LoginWindow, #output {
    background-color:rgb(50, 50, 50);
}


QScrollBar{
    background-color: rgb(80,80,80);
}

Container, LoginWindow, #output {
    border: 2px solid rgb(150, 150, 150);
    border-radius: 4px;
}

#output{
    padding: 3px 5px;
    font-weight:bold;
}

ConfirmButton {
    background-color:rgb(48, 223, 62);
    font-weight: bold;
}

RejectButton {
    background-color:rgb(221, 63, 63);
    font-weight: bold;
}

DefaultButton {
    background-color:rgb(224, 224, 224);
}
"""