// layer is the container defined in user.html
// all of our elements are in layer.children

function selectElem(tag) {
    var elem = null;
    for (var i = 0; i < layer.children.length; i++) {
        if (layer.children[i].id() === tag) {
            elem = layer.children[i];
        }
    }
    return elem;
}

function modifyElem(tag, msg) {
    var elem = selectElem(tag);
    var dx = 10, dy = 10, pzoom = 10/9, nzoom = 9/10, deg = 5;
    switch (msg) {
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
