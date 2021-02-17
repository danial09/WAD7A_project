$(document).ready(function (){
    $(".cell").on("keydown", cellKeyDown);
    $('.cell').focus(onCellFocus)
});

function cellKeyDown(event) {
    event.preventDefault()

    if (!isNaN(parseInt(event.key)) && event.key !== "0" && canEdit(this)) {
        $(this).html(event.key)
        highlightRelatedNum(event.key)
    }
    else if ((event.key === 'Delete' || event.key === 'Backspace') && !$(this).hasClass("fixedCell")) {
        highlightRelatedNum("")
        $(this).empty();
    }
    if (event.key.startsWith("Arrow")) {
        event.preventDefault();
        keyChangeCell(this, event.key)

    }
}

function highlightRelatedNum(num) {
    $(".relatedNumCell").removeClass("relatedNumCell");

    if (num === "") return;
    $(".cell:contains('" + num + "')").addClass("relatedNumCell");
}

function onCellFocus() {
    $("#focusedCell").removeAttr("id");
    if(canEdit(this)) {
        $(this).attr("id", "focusedCell")
    }

    const index = $(this).index();
    // Get all the cells on the board.
    // There's certainly a better way to do this.
    const cells = $(this).parent().children();

    // Highlight cells on same column
    $(".relatedColCell").removeClass("relatedColCell");
    for (let i = index % 9; i < 81; i += 9) {
        if (i === index) continue;
        $(cells[i]).addClass("relatedColCell");
    }

    // Highlight cells on same row
    $(".relatedRowCell").removeClass("relatedRowCell");
    for (let i = 0; i < 9; i++) {
        const offset = 9 * Math.floor(index / 9);
        if (offset + i === index) continue;
        $(cells[offset + i]).addClass("relatedRowCell");
    }

    // Highlight same num
    highlightRelatedNum($(this).text())


    // Highlight sub-grid
    $(".relatedGridCell").removeClass("relatedGridCell");
    // Find starting cell of the sub-grid row
    let startingRowCell;
    if (index < 26)         startingRowCell = 0;
    else if (index < 53)    startingRowCell = 27;
    else                    startingRowCell = 54

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
                $(cell).addClass("relatedGridCell")
        }
    }
}

function keyChangeCell(cell, key) {

    const curPosition = $(cell).index();
    let newPosition = null;

    switch (key) {
        case "ArrowLeft":
            newPosition = (curPosition - 1);
            if (newPosition % 9 === 8 || newPosition === -1) newPosition +=9
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
        setTimeout(function() {
            $(newCell).focus()
        }, 0
        )
    }
}

function canEdit(cell) {
    return !($(cell).hasClass("fixedCell") && !$(cell).hasClass("correctCell"));
}
