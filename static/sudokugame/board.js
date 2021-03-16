$(document).ready(function (){
    $(".cell")
        .on("keydown", cellKeyDown)
        .focus(onCellFocus);
});

function cellKeyDown(event) {
    // First, handle if one of the arrow keys were pressed
    if (event.key.startsWith("Arrow")) {
        event.preventDefault();
        keyChangeCell(this, event.key);
        return;
    }
    // Now, let's handle emptying the cell
    if ((event.key === 'Delete' || event.key === 'Backspace' || event.key === '0') && !$(this).hasClass("fixedCell")) {
        event.preventDefault();
        highlightRelatedNum("");
        $(this).empty();
        return;
    }

    // Finally, let's handle adding a number between 1-9 to the cell
    // Check that the user has inputted a printable character, return if this is not the case.
    if (event.key.length !== 1 && event.key !== "Enter") {
        return;
    }

    event.preventDefault();
    if (!isNaN(parseInt(event.key)) && canEdit(this)) {
        $(this).html(event.key);
        highlightRelatedNum(event.key);
    }

}

function highlightRelatedNum(num) {
    $(".relatedNumCell").removeClass("relatedNumCell");

    if (num === "") return;
    $(".cell:contains('" + num + "')").addClass("relatedNumCell");
}

function onCellFocus() {
    cleanUpHighlighting();

    if(canEdit(this)) {
        $(this).attr("id", "focusedCell");
    }

    const index = $(this).index();
    // Get all the cells on the board.
    // There's certainly a better way to do this.
    const cells = $(this).parent().children();

    // Highlight cells on same column
    for (let i = index % 9; i < 81; i += 9) {
        if (i === index) continue;
        $(cells[i]).addClass("relatedColCell");
    }

    // Highlight cells on same row
    for (let i = 0; i < 9; i++) {
        const offset = 9 * Math.floor(index / 9);
        if (offset + i === index) continue;
        $(cells[offset + i]).addClass("relatedRowCell");
    }

    // Highlight same num
    highlightRelatedNum($(this).text());


    // Now, we highlight the sub-grid
    // Find starting cell of the sub-grid row
    let startingRowCell;
    if (index < 26)         startingRowCell = 0;
    else if (index < 53)    startingRowCell = 27;
    else                    startingRowCell = 54;

    // Find horizontal offset of the starting cell of this sub-grid
    let horizontalOffset;
    const indexMod9 = index % 9;
    if (indexMod9 < 3)      horizontalOffset = 0;
    else if (indexMod9 < 6) horizontalOffset = 3;
    else                    horizontalOffset = 6;

    // Compute starting cell of this sub-grid
    const startingCell = startingRowCell + horizontalOffset;

    for (let i = 0; i < 3; ++ i) {
        for (let j = 0; j < 3; ++j) {
            const cell = $(cells[(startingCell + i) + 9 * j]);
            if (canEdit(cell))
                $(cell).addClass("relatedGridCell");
        }
    }
}

function keyChangeCell(cell, key) {

    const curPosition = $(cell).index();
    let newPosition = null;

    switch (key) {
        case "ArrowLeft":
            newPosition = (curPosition - 1);
            if (newPosition % 9 === 8 || newPosition === -1) newPosition +=9;
            break;

        case "ArrowRight":
            newPosition = (curPosition + 1);
            if (newPosition % 9 === 0 || newPosition === 81) newPosition -= 9;
            break;
        case "ArrowDown":
            if (curPosition < 9*8)  newPosition = curPosition + 9;
            else                    newPosition = curPosition % 9;
            break;
        case "ArrowUp":
            if (curPosition < 9)    newPosition = (9*8) + curPosition;
            else                    newPosition = curPosition - 9;
            break;
    }

    if (newPosition != null) {
        const newCell = $(cell).parent().children("div")[newPosition];
        $(newCell).focus();
    }
}

function cleanUpHighlighting() {
    $("#focusedCell").removeAttr("id");

    const highlightClasses = ["relatedNumCell", "relatedGridCell", "relatedRowCell", "relatedColCell"];
    highlightClasses.forEach(c => $("."+c).removeClass(c));
}

function canEdit(cell) {
    return !($(cell).hasClass("fixedCell") && !$(cell).hasClass("correctCell"));
}
