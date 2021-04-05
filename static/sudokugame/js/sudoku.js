class Sudoku {
    constructor(lives, hints, solutionBoard = null, boardType) {
        this.focusedCell = null;
        this.focusedValue = null;
        this.focusedNotes = null;
        this.timeID = null;
        this.timeElapsed = 0;
        this.solutionBoard = solutionBoard
        this.timeElement = $("#game-time p");
        this.lives = lives;
        this.hints = hints;
        this.boardType = boardType;
    }

    start() {
        this.remaining = 81 - $(".fixed-cell").length;
        Sudoku.setHint(this.hints);
        Sudoku.setLives(this.lives);

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
            } else if (event.key.toLowerCase() === 'h') {
                $("#btn-hint").click();
            } else if (event.key.toLowerCase() === 's') {
                $("#btn-solve").click();
            } else if ((event.key === 'Delete' || event.key === 'Backspace' || event.key === '0') &&
                    !$(this.focusedCell).hasClass("fixed-cell")) {

                $("#focused-cell").children().empty();
                $(".related-num-cell").removeClass("related-num-cell");
            } else if (!isNaN(parseInt(event.key)) && this.focusedCell !== null && !$(this.focusedCell).hasClass("fixed-cell")) {
                this.cellInput(event.key);
            }
        });

        $("#btn-solve").click(() => {
            let solution = null;

            if (this.solutionBoard !== null) {
                solution = this.solutionBoard;
            } else {
                $.ajax({
                    url: 'ajax/solve/',
                    async: false,
                    dataType: 'json',
                    success: function (data) {
                        const solution_str = data.solution;
                        solution = Sudoku.unflattenBoard(solution_str)
                    }
                })
            }
            this.fillBoard(solution)
            this.stopGame();
        });

        $("#btn-hint").click(() => {
            if (this.focusedCell === null || $(this.focusedCell).hasClass("fixed-cell") || this.hints <= 0) return;
            const row = $(this.focusedCell).parent().index();
            const col = $(this.focusedCell).index();
            let value = null;

            if (this.solutionBoard !== null)
            {
                value = this.solutionBoard[row][col];
            } else {
                $.ajax({
                    url: 'ajax/hint/',
                    async: false,
                    data: {
                        'row': row,
                        'col': col
                    },
                    dataType: 'json',
                    success: function (data) {
                        value = data.value;
                    }
                });
            }
            if (value === '0') return;
            $(this.focusedCell)
                .addClass("fixed-cell")
                .find(".cell-value").html(value);

            $(this.focusedNotes).empty();
            this.inputCheck(value);
            this.hints--;
            Sudoku.setHint(this.hints);
        });

        this.startTime();
    }

    stopGame() {
        this.focusedCell = null;
        this.stopTime();
        $("#btn-hint").attr("disabled", true);
        $("#btn-solve").attr("disabled", true);
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

    inputCheck(value) {
        let result = null;
        const row = $(this.focusedCell).parent().index();
        const col = $(this.focusedCell).index();
        let solution = this.solutionBoard;

        if (this.solutionBoard !== null) {
            result = value === this.solutionBoard[row][col] ? "correct" : "incorrect";
        } else {
            $.ajax({
                url: 'ajax/input/',
                async: false,
                data: {
                    'row': row,
                    'col': col,
                    'val': value
                },
                dataType: 'json',
                success: function (data) {
                    result = data.result;
                    solution = Sudoku.unflattenBoard(data.solution);
                }
            });
        }

        if (result === "correct") {
            this.remaining--;
            $(this.focusedCell).addClass("fixed-cell").removeClass("wrong-cell");
            if (this.remaining === 0) {
                this.stopGame();
                this.solutionBoard !== null ? this.generatePracticeSuccess() : this.generateSuccessPage()
            }
        } else {
            if ($(this.focusedValue).html() !== value)
                this.lives--;

            $(this.focusedCell).addClass("wrong-cell");
            Sudoku.setLives(this.lives);
            if (this.lives === 0) {
                this.stopGame();
                this.generateFailurePage();
                this.fillBoard(solution);
            }
        }
    }

    cellInput(key) {
        const inputMode = document.getElementById("btn-input").checked === true ? "input" : "notes";

        if (inputMode === "input") {
            this.focusedNotes.empty();
            this.inputCheck(key);
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

    generatePracticeSuccess() {
        $("#left-panel-wrapper")
            .empty()
            .append($("<h1>Well Done!</h1>"))
            .append($("<h2>You've completed the practice board</h2>"))
            .append($("<p>Why not try your skills in a real game?</p>"))
            .append(
                $("<div class='d-grid gap-2 col-8 mx-auto'></div>")
                    .append($("<button class=\"btn btn-primary\" type=\"button\" onclick=\"document.location.reload()\">Practice Again</button>"))
                    .append($("<button class=\"btn btn-primary\" type=\"button\" data-bs-toggle=\"modal\" data-bs-target=\"#playModal\">New Game</button>"))
            )
    }

    generateSuccessPage() {
        const base = 50;
        const timeBonus = Math.max(15 - Math.floor(this.timeElapsed / 60), 0) * 20;

        const hintBonus = this.hints === 3 ? 100 : 0;
        const livesBonus = this.lives === 3 ? 100 : 0;

        const score = base + timeBonus + hintBonus + livesBonus;

        $("#left-panel-wrapper")
            .empty()
            .append($("<h1>Well Done!</h1>"))
            .append($("<h2>Your Score: " + score +"</h2>"))
            .append($("<p>Base: " + base + "</p>"))
            .append($("<p>Time Bonus: " + timeBonus + "</p>"))
            .append($("<p>Lives Bonus: " + livesBonus + "</p>"))
            .append($("<p>Hints Bonus: " + hintBonus + "</p>"))
            .append(
                $("<div class='d-grid gap-2 col-8 mx-auto'></div>")
                    .append($("<button class=\"btn btn-primary\" type=\"button\" data-bs-toggle=\"modal\" data-bs-target=\"#playModal\">New Game</button>"))
                    .append($("<a href=\"../leaderboard/\" class=\"btn btn-warning\" type=\"button\">Leaderboard</a>"))
            )
    }

    generateFailurePage() {
        const panel = $("#left-panel-wrapper")
            .empty()
            .append($("<h1>Better Luck Next Time</h1>"));

        const buttonDiv = $("<div class='d-grid gap-2 col-8 mx-auto'></div>");

        if (this.boardType === 'DC') {
            $(buttonDiv).append($("<a class=\"btn btn-primary\" type=\"button\" href='../practice/'>Practice for Tomorrow</a>"))
        } else {
            $(buttonDiv).append($("<button class=\"btn btn-primary\" type=\"button\" data-bs-toggle=\"modal\" data-bs-target=\"#playModal\">New Game</button>"));
        }
        $(buttonDiv).append($("<a href=\"../leaderboard/\" class=\"btn btn-warning\" type=\"button\">Leaderboard</a>"))
        $(panel).append(buttonDiv);
    }

    fillBoard(board) {
        const sudokuBoard = $(".game-board");
        sudokuBoard.empty();
        board.forEach(row => {
            const tableRow = $("<tr></tr>").addClass("game-row");
            row.forEach(cell => {
                tableRow.append(
                    $("<td></td>")
                        .addClass("game-cell fixed-cell")
                        .append($("<div></div>").addClass("cell-value").append(cell))
                );
            });
            sudokuBoard.append(tableRow);
        });
    }

    static setHint(hint) {
        $("#game-hints p").html(hint === Infinity ? "&infin;" : hint);
    }

    static setLives(lives) {
        $("#game-lives p").html(lives === Infinity ? "&infin;" : lives);
    }

    static mod(n, m) {
        // Helper function to only get the positive mod result.
        return ((n % m) + m) % m;
    }

    static unflattenBoard(boardStr) {
    let board = []
        for (let i = 0; i < 9; i++) {
            let row = []
            for (let j = 0; j < 9; j++) {
                row.push(boardStr[9*i+j]);
            }
            board.push(row);
        }
        return board;
    }

}
