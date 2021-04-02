$(document).ready(function() {
    $(".game-cell").on("click", (target) => {
        focusCell($(target.target).closest(".game-cell"));
    });
    $("body").keydown((event) => {
        if (event.key.startsWith("Arrow")) {
            cellChangeFocus(event.key);

        } else if ((event.key === 'Delete' || event.key === 'Backspace' || event.key === '0') &&
                !($("#focused-cell").hasClass("fixed-cell"))) {

            $("#focused-cell").children().empty();
            $(".related-grid-cell").removeClass("related-grid-cell");
        } else if (!isNaN(parseInt(event.key))) {
            cellInput(event.key);
        }
    })
})

function mod(n, m) {
    // Function to only get the positive mod result.
    return ((n % m) + m) % m;
}

function highlightRelatedCells(cell) {
    let cellValue = $(cell).find(".cell-value").html();
    if (cellValue === "") cellValue = 0;
    $(".related-grid-cell").removeClass("related-grid-cell");
    $(".cell-value:contains(" + cellValue +")").parent().addClass("related-grid-cell");
}

function focusCell(cell) {
    $("#focused-cell").removeAttr("id");
    $(cell).attr("id", "focused-cell");

    $(".related-row-cell").removeClass("related-row-cell");
    $(cell).siblings().addClass("related-row-cell");

    $(".related-col-cell").removeClass("related-col-cell");
    $(".game-cell:nth-child(" + ($(cell).index() + 1) + ")").addClass("related-col-cell");
    $(cell).removeClass("related-col-cell"); // Probably not necessary.

    highlightRelatedCells(cell);
}

function cellChangeFocus(direction) {
    const curCell = $("#focused-cell");
    const curPosition = $(curCell).index();
    let newCell = null;
    if ($(curCell).length === 0) {
        newCell = $(".game-cell").first();
    } else if (direction === "ArrowRight" || direction === "ArrowLeft") {
        const newPosition = mod(curPosition + (direction === "ArrowRight" ? 1 : -1), 9);
        newCell = curCell.parent().children()[newPosition];
    } else {
        const curRow = $(curCell).parent();
        const newRowPosition = mod($(curRow).index() + (direction === "ArrowDown" ? 1 : -1), 9);
        const newRow = $(curRow).parent().children()[newRowPosition];
        newCell = $(newRow).children()[curPosition];
    }
    focusCell(newCell);
}

function cellInput(key) {
    const inputMode = document.getElementById("btn-input").checked === true ? "input" : "notes";
    const valueGrid = $("#focused-cell").find(".cell-value");
    const notesGrid = $("#focused-cell").find(".notes-grid");

    if (inputMode === "input") {
        notesGrid.empty();
        // TODO: Add an AJAX call here to validate user input
        valueGrid.html(key);
        highlightRelatedCells($("#focused-cell"));
    } else {
        valueGrid.empty();
        const existingNote = $(notesGrid).find($(":contains(" + key + ")"))
        if (existingNote.length !== 0) {
            $(existingNote).remove();
        } else {
            const newNote = $("<div></div>").addClass("notes-grid-cell").append(key);
            notesGrid.append(newNote)
        }
    }
}
