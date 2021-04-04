class Sudoku {
    constructor(lives, hints) {
        this.focusedCell = null;
        this.focusedValue = null;
        this.focusedNotes = null;
        this.timeID = null;
        this.timeElapsed = 0;
        this.timeElement = $("#game-time p");
        this.lives = lives;
        this.livesElement = $("#game-lives p");
        this.hints = hints;
        this.hintsElement = $("#game-hints p");
    }

    start() {
        $(".game-cell").on("click", (target) => {
            this.focusCell($(target.target).closest(".game-cell"));
        });

        $("body").keydown((event) => {
            if (event.key.toLowerCase() === 'n') {
                $("#btn-notes").click();
            } else if (event.key.toLowerCase() === 'i') {
                $("#btn-input").click();
            } else if (event.key.startsWith("Arrow")) {
                this.cellChangeFocus(event.key);

            } else if ((event.key === 'Delete' || event.key === 'Backspace' || event.key === '0') &&
                    !$(this.focusedCell).hasClass("fixed-cell")) {

                $("#focused-cell").children().empty();
                $(".related-num-cell").removeClass("related-num-cell");
            } else if (!isNaN(parseInt(event.key)) && this.focusedCell !== null && !$(this.focusedCell).hasClass("fixed-cell")) {
                this.cellInput(event.key);
            }
        });

        this.startTime();
    }

    startTime() {
        this.timeElapsed = 0;
        this.timeID = setInterval(() => {
            this.timeElapsed++;
            const minutes = Math.floor(this.timeElapsed / 60);
            const seconds = this.timeElapsed % 60;
            this.timeElement.html(minutes + ":" + (seconds < 10 ? "0" : "") + seconds);
        }, 1000);

    }

    stopTime() {
        clearInterval(this.timeID);
    }

    focusCell(cell) {
        $(this.focusedCell).removeAttr("id");
        this.focusedCell = cell;
        this.focusedValue = $(cell).find(".cell-value");
        this.focusedNotes = $(cell).find(".notes-grid");

        $(this.focusedCell).attr("id", "focused-cell");

        this.highlightRelatedCells();
        this.highlightRowCol();
        this.highlightSubgrid();
    }

    cellChangeFocus(direction) {
        const curPosition = $(this.focusedCell).index();
        let newCell;
        if (this.focusedCell === null) {
            newCell = $(".game-cell").first();
        } else if (direction === "ArrowRight" || direction === "ArrowLeft") {
            const newPosition = Sudoku.mod(curPosition + (direction === "ArrowRight" ? 1 : -1), 9);
            newCell = $(this.focusedCell).parent().children()[newPosition];
        } else {
            const curRow = $(this.focusedCell).parent();
            const newRowPosition = Sudoku.mod($(curRow).index() + (direction === "ArrowDown" ? 1 : -1), 9);
            const newRow = $(curRow).parent().children()[newRowPosition];
            newCell = $(newRow).children()[curPosition];
        }
        this.focusCell(newCell);
    }

    highlightRowCol() {
        $(".related-row-cell").removeClass("related-row-cell");
        $(this.focusedCell).siblings().addClass("related-row-cell");

        $(".related-col-cell").removeClass("related-col-cell");
        $(".game-cell:nth-child(" + ($(this.focusedCell).index() + 1) + ")").addClass("related-col-cell");
        $(this.focusedCell).removeClass("related-col-cell"); // Probably not necessary.
    }

    highlightRelatedCells() {
        $(".related-num-cell").removeClass("related-num-cell");

        let cellValue = $(this.focusedValue).html();
        if (cellValue === "") cellValue = '0';
        $(".cell-value:contains(" + cellValue +")").parent().addClass("related-num-cell");
    }

    highlightSubgrid() {
        $(".related-grid-cell").removeClass("related-grid-cell");

        const gridStartColumn = Math.floor($(this.focusedCell).index() / 3) * 3;
        const gridStartRow = Math.floor($(this.focusedCell).parent().index() / 3) * 3;

        const rows = $(".game-row");
        for (let i = gridStartRow; i < gridStartRow + 3; i++) {
            const cells = $(rows[i]).find(".game-cell");
            for (let j = gridStartColumn; j < gridStartColumn + 3; j++) {
                if (cells[j] !== this.focusedCell) {
                    $(cells[j]).addClass("related-grid-cell")
                }
            }
        }
    }

    cellInput(key) {
        const inputMode = document.getElementById("btn-input").checked === true ? "input" : "notes";

        if (inputMode === "input") {
            this.focusedNotes.empty();
            // TODO: Add an AJAX call here to validate user input
            this.focusedValue.html(key);
            this.highlightRelatedCells($("#focused-cell"));
        } else {
            this.focusedValue.empty();
            $(".related-num-cell").removeClass("related-num-cell");
            const existingNote = $(this.focusedNotes).find($(":contains(" + key + ")"))
            if (existingNote.length !== 0) {
                $(existingNote).remove();
            } else {
                const newNote = $("<div></div>").addClass("notes-grid-cell").append(key);
                this.focusedNotes.append(newNote)
            }
        }
    }

    static mod(n, m) {
        // Helper function to only get the positive mod result.
        return ((n % m) + m) % m;
    }
}
