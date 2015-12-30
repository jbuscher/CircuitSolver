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
                this.classList.add('selected-node');
                var neighbors = getNeighbors(this);
                setupSecondClick(this, neighbors);
            };
        }
    }

    function setupSecondClick(clickedNode, neighbors) {
        var clickedID = clickedNode.id;
        var nodes = $(".circuit-node");
        for(var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            if (neighbors.indexOf(node.id) > -1) {
                node.onclick = function() {
                    drawFromTo(clickedNode, this);
                }
            } else if (node.id == clickedID) {
                //reset state
                node.classList.remove('clickable');
                node.onclick = function() {
                    resetState();
                    this.classList.remove('selected-node');
                    setNodesInitialOnClick();
                }
            } else {
                node.classList.add('not-clickable');
                node.classList.remove('clickable');
            }
        }
    }

    function drawFromTo(startNode, endNode) {
        var splitStart = startNode.id.split(',');
        var splitEnd = endNode.id.split(',');
        var start = {"row":parseInt(splitStart[1]), "col":parseInt(splitStart[2])};
        var end = {"row":parseInt(splitEnd[1]), "col":parseInt(splitEnd[2])};
        var table = $("#circuit-table");
        var height = table.height();
        var width = table.width();

        //MARK jbuscher - likely have to change these moving forward
        var calculatedWidth = width/COLS;
        var calculatedHeight = height/ROWS;
        

    }

    function getNeighbors(node) {
        var neighbors = [];
        var id = node.id.split(",");;
        var row = parseInt(id[1]);
        var col = parseInt(id[2]);
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
        return neighbors;
    }

    function resetState() {
        var nodes = $(".circuit-node");
        for(var i = 0 ; i < nodes.length; i++) {
            nodes[i].classList.remove('not-clickable');
            nodes[i].classList.add('clickable');
        }
    }

})();