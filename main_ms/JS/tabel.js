// script.js

function deleteRow(button) {
    var row = button.parentNode.parentNode;
    var table = row.parentNode;
    table.removeChild(row);
}
