APPBG = "rgb(37, 37, 37)"


appStyles = """
#iGPMT {
    background-color: """+APPBG+""";
}


Heading {
    font-weight: bold;
}

DetailRow {
    padding: 3px 3px;
}

DetailRow:hover {
    background-color:black;
}



Text, QLabel, Heading, QListView, #operationsCont {
    color:white;
    font-size: 16px;
}

QListView, Container, #operationsCont {
    background-color:rgb(50, 50, 50);
}

ConfirmButton {
    background-color:rgb(48, 223, 62);
}

RejectButton {
    background-color:rgb(221, 63, 63);
}

DefaultButton {
    background-color:rgb(224, 224, 224);
}
"""