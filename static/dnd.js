// http://www.html5rocks.com/en/tutorials/dnd/basics/

if (!Modernizr.draganddrop) {
    alert("Hey! Listen! Your browser doesn't support drag and drop.");
}

var dragSource = null;
function handleDragStart(e) {
    this.classList.add('selected');

    dragSource = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }

    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    this.classList.add('over');
}

function handleDragLeave(e) {
    this.classList.remove('over');
}

function handleDrop(e) {
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
    this.classList.remove('selected');
}

var magicBoxes = $('.magic');

$(magicBoxes).each(function( index ) {
    this.addEventListener('dragstart', handleDragStart, false);
    this.addEventListener('dragenter', handleDragEnter, false);
    this.addEventListener('dragover', handleDragOver, false);
    this.addEventListener('dragleave', handleDragLeave, false);
    this.addEventListener('drop', handleDrop, false);
    this.addEventListener('dragend', handleDragEnd, false);
});
