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