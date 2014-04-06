// http://www.html5rocks.com/en/tutorials/dnd/basics/

if (!Modernizr.draganddrop) {
    alert("Hey! Listen! Your browser doesn't support drag and drop.");
}

var dragSource = null;
function handleDragStart(e) {
    console.log('handleDragStart');
    this.classList.add('selected');

    dragSource = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragOver(e) {
    console.log('handleDragOver');
    if (e.preventDefault) {
        e.preventDefault();
    }

    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    console.log('handleDragEnter');
    this.classList.add('over');
}

function handleDragLeave(e) {
    console.log('handleDragLeave');
    this.classList.remove('over');
}

function handleDrop(e) {
    console.log('handleDrop');
    if (e.stopPropagation) {
        e.stopPropagation();
    }

    if (dragSource != this) {
        dragSource.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');
    }

    dragSource.classList.remove('selected');
    this.classList.remove('over');

    return false;
}

function handleDragEnd(e) {
    console.log('handleDragEnd');
    this.classList.remove('selected');
}

var magicBoxes = $(".magic");

$(magicBoxes).each(function( index ) {
    this.addEventListener('dragstart', handleDragStart, false);
    this.addEventListener('dragenter', handleDragEnter, false);
    this.addEventListener('dragover', handleDragOver, false);
    this.addEventListener('dragleave', handleDragLeave, false);
    this.addEventListener('drop', handleDrop, false);
    this.addEventListener('dragend', handleDragEnd, false);
});
