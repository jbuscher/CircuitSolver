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
                htmlString += "<td id='node," + i +","+ j + "' class='circuit-node clickable'>" + "&#8226;"+ "</td>";
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
                setOnHovers(this, neighbors);
                setNodesSecondOnClick(neighbors);
            };
        }
    }

    function setNodesSecondOnClick(neighbors) {

    }

    function setOnHovers(clickedNode, neighbors) {
        var clickedID = clickedNode.id;
        var nodes = $(".circuit-node");
        for(var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            if (neighbors.indexOf(node.id) > -1) {
            } else if (node.id == clickedID) {
            } else {
                nodes[i].classList.add('not-clickable');
                nodes[i].classList.remove('clickable');
            }
        }
    }

    function getNeighbors(node) {
        var neighbors = [];
        var id = node.id.split(",");;
        var row = parseInt(id[1]);
        var col = parseInt(id[2]);

        console.log(row + "," + col);
        //top neighbor
        if(row > 0) {
            neighbors.push("node," + (row-1) + "," + col);
        } else {
            neighbors.push(null);
        }
        //right neighbor
        if(col < COLS - 1) {
            neighbors.push("node," + row + "," + (col+1));
        } else {
            neighbors.push(null);
        }
        //bottom neighbor
        if(row < ROWS-1) {
            neighbors.push("node," + (row+1) + "," + col);
        } else {
            neighbors.push(null);
        }
        //left neighbor
        if(col > 0) {
            neighbors.push("node," + row + "," + (col-1));
        } else {
            neighbors.push(null);
        }
        console.log(neighbors);
        return neighbors;
    }

})();