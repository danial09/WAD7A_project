$(document).ready(function() {
    $(".game-cell").on("click", (target) => {
        focusCell($(target.target).closest(".game-cell"));
    });
})

function focusCell(cell) {
    $("#focused-cell").removeAttr("id");
    $(cell).attr("id", "focused-cell");

    $(".related-row-cell").removeClass("related-row-cell");
    $(cell).siblings().addClass("related-row-cell");

    $(".related-col-cell").removeClass("related-col-cell");
    $(".game-cell:nth-child(" + ($(cell).index() + 1) + ")").addClass("related-col-cell");
    $(cell).removeClass("related-col-cell"); // Probably not necessary.

}

function cellKeyDown(cell, event) {
    console.log(event.key + " pressed on cell: " + $(cell));
}
