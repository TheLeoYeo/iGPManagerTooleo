APPBG = "rgb(37, 37, 37)"


appStyles = """
QMainWindow {
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

ContainerFrame, LoginWindow, ModifierWidget, #output {
    background-color:rgb(50, 50, 50);
}


QScrollBar{
    background-color: rgb(80,80,80);
}

Container, LoginWindow, ModifierWidget, #output {
    border: 2px solid rgb(150, 150, 150);
    border-radius: 4px;
}

ModifierWidget:hover{
    background-color:rgb(30, 30, 30);
}

#output{
    padding: 3px 5px;
    font-weight:bold;
}

ConfirmButton {
    background-color:rgb(48, 223, 62);
}

RejectButton {
    background-color:rgb(221, 63, 63);
}

ConfirmButton, RejectButton {
    font-weight: bold;
    padding: 0px 10px;
}

DefaultButton {
    background-color:rgb(224, 224, 224);
}
"""