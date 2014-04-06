var newInstructions;

function processInstructions(inst) {
    while (inst.length > 0) {
        var one = inst.shift();
        if (one.length > 0) {
            console.log(one);
            modifyElem(one);
        }
    }
}

function readInstructions(file) {
    file = file || 'instructions';
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {
                var inst = $.trim(rawFile.responseText);
                processInstructions(inst.split('\n'));
            }
        }
    };
    rawFile.send();
}

var interval = setInterval(readInstructions, 30);
function c() {clearInterval(interval);};
