function requiredObelisk() {
    var emptyPC = document.forms["form1"]["msg_pc"].value;
    var emptyMobile = document.forms["form1"]["msg_mobile"].value;
    if (emptyPC == emptyMobile) {
        return false;
    }
}

function required() {
    var empty = document.forms["form1"]["q"].value;
    if (empty == "") {
        return false;
    }
}

function mbar(sobj) {
    var docurl = sobj.options[sobj.selectedIndex].value;
    if (docurl != "") {
        open(docurl, '_self');
        sobj.selectedIndex = 0;
        sobj.blur();
    }
}

function ClearTextArea() {
    document.getElementById("msg_pc").value = "";
    document.getElementById("msg_mobile").value = "";
}