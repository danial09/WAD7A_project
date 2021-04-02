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
    const col_position = $(cell).index();
    const selector = $(":nth-child(" + (col_position + 1) + ")");
    $(cell).parent().siblings().find(selector).addClass("related-col-cell");
    // $(cell).parent().siblings().each(() => console.log($(this).prop("tagName")));

}

function cellKeyDown(cell, event) {
    console.log(event.key + " pressed on cell: " + $(cell));
}
