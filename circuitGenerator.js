(function() {
"use strict"

var $ = function(search) {
    return document.getElementById(search);     // alias getElementById to simplify lines
};


var ROWS=9;
var COLS=14;
var selectedType = ""

    window.onload = function() {
        generateCircuitItems();
        $("solve-button").onclick = solveRequest;
    };


/*
make a request to the php file to solve the circuit
*/
    function solveRequest() {

    }

    function generateCircuitItems() {
        var circuitArea = $("circuit-area");
        var count = 0;
        for(var i = 0; i < ROWS; i++) {
            for(var j = 0; j < COLS; j++) {
                var square = document.createElement("div");
                square.classList.add("node");
                circuitArea.appendChild(square);
            }
        }
    }

})();