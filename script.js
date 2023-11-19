document.addEventListener("DOMContentLoaded", function () {
    let size = 4;
    let gameContainer = document.getElementById("game-container");
    let gameBoard = document.getElementById("game-board");
    let scoreElement = document.getElementById("score");
    let restartButton = document.getElementById("restart-button");
    let restartButtonScore = document.getElementById("restart-button-score");

    let grid = initializeGrid();
    let score = 0;

    function initializeGrid() {
        let grid = [];
        for (let i = 0; i < size; i++) {
            grid[i] = [];
            for (let j = 0; j < size; j++) {
                grid[i][j] = 0;
            }
        }
        addNewTile(grid);
        addNewTile(grid);
        return grid;
    }

    function addNewTile(grid) {
        let availableCells = [];
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (grid[i][j] === 0) {
                    availableCells.push({ x: i, y: j });
                }
            }
        }
        if (availableCells.length > 0) {
            let randomCell = availableCells[Math.floor(Math.random() * availableCells.length)];
            grid[randomCell.x][randomCell.y] = Math.random() < 0.9 ? 2 : 4;
        }
    }

    function restartGame() {
        grid = initializeGrid();
        score = 0;
        document.getElementById("game-over-overlay").style.display = "none";
        updateGame();
    }

    function moveLeft() {
        let moved = false;
        for (let i = 0; i < size; i++) {
            for (let j = 1; j < size; j++) {
                if (grid[i][j] !== 0) {
                    let k = j;
                    while (k > 0 && grid[i][k - 1] === 0) {
                        grid[i][k - 1] = grid[i][k];
                        grid[i][k] = 0;
                        k--;
                        moved = true;
                    }
                    if (k > 0 && grid[i][k - 1] === grid[i][k]) {
                        grid[i][k - 1] *= 2;
                        score += grid[i][k - 1];
                        grid[i][k] = 0;
                        moved = true;
                    }
                }
            }
        }
        return moved;
    }

    function moveRight() {
        let moved = false;
        for (let i = 0; i < size; i++) {
            for (let j = size - 2; j >= 0; j--) {
                if (grid[i][j] !== 0) {
                    let k = j;
                    while (k < size - 1 && grid[i][k + 1] === 0) {
                        grid[i][k + 1] = grid[i][k];
                        grid[i][k] = 0;
                        k++;
                        moved = true;
                    }
                    if (k < size - 1 && grid[i][k + 1] === grid[i][k]) {
                        grid[i][k + 1] *= 2;
                        score += grid[i][k + 1];
                        grid[i][k] = 0;
                        moved = true;
                    }
                }
            }
        }
        return moved;
    }

    function moveUp() {
        let moved = false;
        for (let j = 0; j < size; j++) {
            for (let i = 1; i < size; i++) {
                if (grid[i][j] !== 0) {
                    let k = i;
                    while (k > 0 && grid[k - 1][j] === 0) {
                        grid[k - 1][j] = grid[k][j];
                        grid[k][j] = 0;
                        k--;
                        moved = true;
                    }
                    if (k > 0 && grid[k - 1][j] === grid[k][j]) {
                        grid[k - 1][j] *= 2;
                        score += grid[k - 1][j];
                        grid[k][j] = 0;
                        moved = true;
                    }
                }
            }
        }
        return moved;
    }

    function moveDown() {
        let moved = false;
        for (let j = 0; j < size; j++) {
            for (let i = size - 2; i >= 0; i--) {
                if (grid[i][j] !== 0) {
                    let k = i;
                    while (k < size - 1 && grid[k + 1][j] === 0) {
                        grid[k + 1][j] = grid[k][j];
                        grid[k][j] = 0;
                        k++;
                        moved = true;
                    }
                    if (k < size - 1 && grid[k + 1][j] === grid[k][j]) {
                        grid[k + 1][j] *= 2;
                        score += grid[k + 1][j];
                        grid[k][j] = 0;
                        moved = true;
                    }
                }
            }
        }
        return moved;
    }

    function updateGame() {
        generateGameTiles(grid);
        scoreElement.textContent = score;
        restartButtonScore.style.display = "block";
        if (isGameOver()) {
            showGameOverOverlay();
            restartButtonScore.style.display = "none";
        }
    }

    function generateGameTiles(grid) {
        gameBoard.innerHTML = "";
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                let tileValue = grid[i][j];
                let tile = document.createElement("div");
                tile.className = "tile";
                tile.textContent = tileValue !== 0 ? tileValue : "";
                tile.style.backgroundColor = getTileColor(tileValue);
                tile.style.color = getTileTextColor(tileValue);
                tile.style.fontSize = getTileFontSize(tileValue);
                gameBoard.appendChild(tile);
            }
        }
    }
    
    function getTileTextColor(value) {
        return (value === 2 || value === 4) ? "#808080" : "#ffffff";
    }
    
    function getTileFontSize(value) {
        if (value > 99) {
            return "45px";
        } else if (value < 100) {
            return "55px";
        }
    }    
    
    function getTileColor(value) {
        switch (value) {
            case 2: return "#eee4da";
            case 4: return "#ede0c8";
            case 8: return "#f2b179";
            case 16: return "#f59563";
            case 32: return "#f67c5f";
            case 64: return "#f65e3b";
            case 128: return "#edcf72";
            case 256: return "#edcc61";
            case 512: return "#edc850";
            case 1024: return "#edc53f";
            case 2048: return "#edc22e";
            default: return "#ccc0b3";
        }
    }

    function handleKeyPress(event) {
        if (!isGameOver()) {
            let moved = false;
            switch (event.key) {
                case "ArrowLeft":
                    moved = moveLeft();
                    break;
                case "ArrowRight":
                    moved = moveRight();
                    break;
                case "ArrowUp":
                    moved = moveUp();
                    break;
                case "ArrowDown":
                    moved = moveDown();
                    break;
            }
            if (moved) {
                addNewTile(grid);
                updateGame();
            }
        }
    }

    function isGameOver() {
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (grid[i][j] === 0) {
                    return false;
                }
                if (i < size - 1 && grid[i][j] === grid[i + 1][j]) {
                    return false;
                }
                if (j < size - 1 && grid[i][j] === grid[i][j + 1]) {
                    return false;
                }
            }
        }
        return true;
    }    

    function showGameOverOverlay() {
        let gameOverOverlay = document.getElementById("game-over-overlay");
        gameOverOverlay.style.display = "flex";
    }

    document.addEventListener("keydown", handleKeyPress);
    restartButton.addEventListener("click", restartGame);
    restartButtonScore.addEventListener("click", restartGame);

    updateGame();
});
