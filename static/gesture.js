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

function select(elem) {
    console.log(elem);
    if (elem != null) {
        elem.opacity(0.6);
        layer.draw();
        currentElem = elem;
    }
}

function unselect(elem) {
    console.log(elem);
    if (elem != null) {
        elem.opacity(0.9);
        layer.draw();
        currentElem = null;
    }
}

function modifyElem(msg) {
    var elem = layer.children[currentElemIndex];
    var dx = 10, dy = 10, pzoom = 20/19, nzoom = 19/20, deg = 1;
    var right = screen.width - elem.width() - elem.x();
    var bottom = screen.height - elem.height() - elem.y();

    switch (msg) {
    case "next element":
        unselect(currentElem);
        currentElemIndex = (currentElemIndex + 1) % layer.children.length;
        select(layer.children[currentElemIndex]);
        break;
    case "left":
        elem.move({x:-Math.min(dx, elem.x()), y:0});
        break;
    case "right":
        elem.move({x:Math.min(dx, right), y:0});
        break;
    case "up":
        elem.move({x:0, y:Math.min(dy, bottom)});
        break;
    case "down":
        elem.move({x:0, y:-Math.min(dy, elem.y())});
        break;
    case "zoom in":
        var new_scale = Math.min(elem.getScaleX() * pzoom, 1.5);
        elem.setScaleX(new_scale);
        elem.setScaleY(new_scale);
        break;
    case "zoom out":
        var new_scale = Math.max(elem.getScaleX() * nzoom, 0.5);
        elem.setScaleX(new_scale);
        elem.setScaleY(new_scale);
        break;
    case "rotate right":
        elem.rotateDeg(deg);
        break;
    case "rotate left":
        elem.rotateDeg(-deg);
        break;
    }
    layer.draw();
}

modifyElem('next element');
