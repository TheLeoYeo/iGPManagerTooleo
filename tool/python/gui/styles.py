APPBG = "rgb(37, 37, 37)"


appStyles = """
#iGPMT {
    background-color: """+APPBG+""";
}

Heading {
    font-weight: bold;
}

BaseRow {
    padding: 6px 6px;
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

ContainerFrame, LoginWindow {
    background-color:rgb(50, 50, 50);
}


QScrollBar{
    background-color: rgb(80,80,80);
}

Container, LoginWindow {
    border: 2px solid rgb(150, 150, 150);
    border-radius: 4px;
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