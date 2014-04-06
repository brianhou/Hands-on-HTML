// layer is the container defined in user.html
// all of our elements are in layer.children

function selectElemByTag(tag) {
    var elem = null;
    for (var i = 0; i < layer.children.length; i++) {
        if (layer.children[i].id() === tag) {
            elem = layer.children[i];
        }
    }
    return elem;
}

var currentElem, currentElemIndex = 0;
var grabbed = true;

$(document).click(function (evt) {
    grabbed = !grabbed;
    console.log(grabbed);
    if (!grabbed) {
        unselect(currentElem);
    } else {
        select(currentElem);
    }
    return false;
});

function select(elem) {
    console.log(elem);
    if (elem != null) {
        elem.opacity(0.2);
        layer.draw();
        currentElem = elem;
    }
}

function unselect(elem) {
    console.log(elem);
    if (elem != null) {
        elem.opacity(1);
        layer.draw();
        currentElem = null;
    }
}

function modifyElem(msg) {
    if (!grabbed) { // only perform actions if element is grabbed
        console.log("hey you ain't grabbin' anything");
        return;
    }

    var elem = layer.children[currentElemIndex];
    var dx = 10, dy = 10, pzoom = 10/9, nzoom = 9/10, deg = 5;

    switch (msg) {
    case "next element":
        unselect(currentElem);
        currentElemIndex = (currentElemIndex + 1) % layer.children.length;
        select(layer.children[currentElemIndex]);
        break;
    case "left":
        elem.move({x:-dx, y:0});
        break;
    case "right":
        elem.move({x:dx, y:0});
        break;
    case "up":
        elem.move({x:0, y:dy});
        break;
    case "down":
        elem.move({x:0, y:-dy});
        break;
    case "zoom in":
        elem.setScaleX(elem.getScaleX()*pzoom);
        elem.setScaleY(elem.getScaleY()*pzoom);
        break;
    case "zoom out":
        elem.setScaleX(elem.getScaleX()*nzoom);
        elem.setScaleY(elem.getScaleY()*nzoom);
        break;
    case "rotate right":
        elem.rotate(deg);
        break;
    case "rotate left":
        elem.rotate(-deg);
        break;
    }
    layer.draw();
}

modifyElem('next element');
