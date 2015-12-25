(function() {

var ROWS=9;
var COLS=14;

    $(document).ready(function() {
        generateCircuitItems(ROWS,COLS);
    })

    function generateCircuitItems(rows, cols) {
        var tableDiv = $("#circuit-grid");
        var htmlString = "";
        var count = 0;
        htmlString += "<table id='circuit-table'>";
        for(var i = 0; i < rows; i++) {
            htmlString += "<tr id='row," + i + "' class='circuit-row'>"
            for(var j = 0; j < cols; j++) {
                htmlString += "<td id='node," + i +","+ j + "' class='circuit-node'>" + "&#8226;"+ "</td>";
                count++;
            }
            htmlString += "</tr>"
        }
        htmlString += "</tr>"
        tableDiv.append(htmlString);
    }

})();