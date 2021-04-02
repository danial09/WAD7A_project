$(document).ready(function() {
    $(".game-cell").on("click", (target) => {
        focusCell($(target.target).closest(".game-cell"));
    });
    $("body").keydown((event) => {
        console.log(event.key);
        if (event.key.startsWith("Arrow")) {
            event.preventDefault();
            cellChangeFocus(event.key);
        }
    })
})

function mod(n, m) {
    // Function to only get the positive mod result.
    return ((n % m) + m) % m;
}

function focusCell(cell) {
    $("#focused-cell").removeAttr("id");
    $(cell).attr("id", "focused-cell");

    $(".related-row-cell").removeClass("related-row-cell");
    $(cell).siblings().addClass("related-row-cell");

    $(".related-col-cell").removeClass("related-col-cell");
    $(".game-cell:nth-child(" + ($(cell).index() + 1) + ")").addClass("related-col-cell");
    $(cell).removeClass("related-col-cell"); // Probably not necessary.

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
