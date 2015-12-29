(function() {
"use strict"

var ROWS=9;
var COLS=14;

    $(document).ready(function() {
        generateCircuitItems();
        setNodesInitialOnClick();
    })

    function generateCircuitItems() {
        var tableDiv = $("#circuit-grid");
        var htmlString = "";
        var count = 0;
        htmlString += "<table id='circuit-table'>";
        for(var i = 0; i < ROWS; i++) {
            htmlString += "<tr id='row," + i + "' class='circuit-row'>"
            for(var j = 0; j < COLS; j++) {
                htmlString += "<td id='node," + i +","+ j + "' class='circuit-node'>" + "&#8226;"+ "</td>";
                count++;
            }
            htmlString += "</tr>"
        }
        htmlString += "</tr>"
        tableDiv.append(htmlString);
    }


    function setNodesInitialOnClick() {
        var nodes = $(".circuit-node");
        for(var i = 0; i < nodes.length; i++) {
            nodes[i].onclick = function() {
                var neighbors = getNeighbors(this);
                setOnHovers(neighbors);
                setNodesSecondOnClick(neighbors);
            };
        }
    }

    function setNodesSecondOnClick(neighbors) {

    }

    function setOnHovers(neighbors) {
        var nodes = $(".circuit-node");
        for()
    }

    function getNeighbors(node) {
        var neighbors = [];
        var id = node.id.split(",");;
        var row = parseInt(id[1]);
        var col = parseInt(id[2]);

        console.log(row + "," + col);
        //top neighbor
        if(row > 0) {
            var top = $("#node," + (row-1) + "," + col);
            neighbors.push(top);
        } else {
            neighbors.push(null);
        }
        //right neighbor
        if(col < COLS - 1) {
            var right = $("#node," + row + "," + (col+1));
            neighbors.push(right);
        } else {
            neighbors.push(null);
        }
        //bottom neighbor
        if(row < ROWS-1) {
            var bottom = $("#node," + (row+1) + "," + col);
            neighbors.push(bottom);
        } else {
            neighbors.push(null);
        }
        //left neighbor
        if(col > 0) {
            var left = $("#node," + row + "," + (col-1));
            neighbors.push(left);
        } else {
            neighbors.push(null);
        }
        console.log(neighbors);
        return neighbors;
    }

})();