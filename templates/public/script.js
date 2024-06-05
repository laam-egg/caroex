// const gameInfoList = [
//     {
//         room_id: "ROOM 1",
//         match_id: "MATCH 1",
//         status: undefined,
//         size: 12,
//         board: [
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//         ],
//         time1: 0.0,
//         time2: 0.0,
//         team1_id: "1+x",
//         team2_id: "2+o",
//         turn: "1+x",
//         score1: 0,
//         score2: 0,
//     },

//     {
//         room_id: "ROOM 1",
//         match_id: "MATCH 1",
//         status: undefined,
//         size: 12,
//         board: [
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
//         ],
//         time1: 0.0,
//         time2: 0.0,
//         team1_id: "1+x",
//         team2_id: "2+o",
//         turn: "1+x",
//         score1: 0,
//         score2: 0,
//     }
// ];

const gameInfoList = JSON.parse(document.getElementById("game-info-list-json").value);

let game = gameInfoList[0];
let currentGameInfoIndex = 0;

const updateCurrentGameInfo = () => {
    console.log("this func")

    {
        document.getElementById("next-move").style.display = "block";
        document.getElementById("prev-move").style.display = "block";
    }

    if (currentGameInfoIndex <= 0) {
        currentGameInfoIndex = 0;
        document.getElementById("prev-move").style.display = "none";
    }
    
    if (currentGameInfoIndex >= gameInfoList.length - 1) {
        currentGameInfoIndex = gameInfoList.length - 1;
        document.getElementById("next-move").style.display = "none";
    }

    game = gameInfoList[currentGameInfoIndex];

    if (game.status != "None" && game.status != undefined) {
        // End the game
        document.getElementById("status").style.display = "block";
        // document.getElementsByClassName("gameboard")[0].style.display = "none";
        document.getElementById("status").innerText = game.status;
        // prevMatchId = game.match_id
    } else {
        document.getElementById("status").style.display = "none";
        document.getElementById("status").innerText = "";
    }

    drawBoard();
    render();
}

updateCurrentGameInfo();

const next = () => {
    ++currentGameInfoIndex;
    updateCurrentGameInfo();
}

const prev = () => {
    --currentGameInfoIndex;
    updateCurrentGameInfo();
}

window.addEventListener('keydown', (event) => {
    if (event.isComposing || event.keyCode === 229) {
        return;
    }

    switch (event.key) {
        case "ArrowLeft":
            prev();
            break;
        
        case "ArrowRight":
            next();
            break;
        
        default:
            return;
    }

    event.preventDefault();
});

var prevGameBoard;
function drawBoard() {
    document.getElementsByClassName("gameboard")[0].style.display = "block";
    document.getElementById("roomid-input-container").style.display="none";
    if (game.status == "None"){
        document.getElementById("status").style.display = "none";
        document.getElementById("confirm-button-container").style.display = "none";
    }

    var size = game.size;
    var gameBoard = document.getElementsByClassName("gameboard");
    var gameBoardHTML = "<table cell-spacing = '0'>";

    const num_cells = size + 1;
    const max_width = 600;
    const max_height = 400;

    gameBoardHTML += "<tr>";
    gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300;'>`
                + "</td>";
    for (var i = 0; i < size; i++) {
        gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300;'>`
            + i
            + "</td>";
    }
    gameBoardHTML += "</tr>";

    for (var i = 0; i < size; i++) {
        gameBoardHTML += "<tr>"
        gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300;'>`
                + i
                + "</td>"
        for (var j = 0; j < size; j++) {

            if (prevGameBoard != undefined && game.board[i][j] == 'x' && prevGameBoard[i][j] === ' ') {
                gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300; color: rgb(254,96,93); background-color: rgba(238, 238, 238, 0.5); border: 3px solid rgb(254,96,93); border-collapse: collapse;'>`
                    + game.board[i][j]
                    + "</td>"
            }
            else if (prevGameBoard != undefined && game.board[i][j] == 'o' && prevGameBoard[i][j] === ' ') {
                gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300; color: #3DC4F3; background-color: rgba(238, 238, 238, 0.5); border: 3px solid #3DC4F3; border-collapse: collapse;'>`
                    + game.board[i][j]
                    + "</td>"
            }

            else if (game.board[i][j] == 'x'){
                gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300; color: rgb(254,96,93)'>`
                + game.board[i][j]
                + "</td>"
            }
            else {
                gameBoardHTML += `<td style='width:${max_width / num_cells}px; height:${max_width / num_cells}px; font-size:${max_height / num_cells}px; font-weight: 300; color: #3DC4F3'>`
                + game.board[i][j]
                + "</td>"
            }

        }
        gameBoardHTML += "</tr>";
    }
    prevGameBoard = game.board;
    gameBoardHTML += "</table>";
    gameBoard[0].innerHTML = gameBoardHTML;

}

function render() {
    if (game.turn === game.team1_id) {
        document.getElementById('turn-flag-2').style.visibility = "hidden"
        document.getElementById('turn-flag-1').style.visibility = "visible"
    }
    else if (game.turn === game.team2_id) {
        document.getElementById('turn-flag-2').style.visibility = "visible"
        document.getElementById('turn-flag-1').style.visibility = "hidden"
    }
    else if (game.turn == undefined){
        document.getElementById('turn-flag-2').style.visibility = "hidden"
        document.getElementById('turn-flag-1').style.visibility = "hidden"
    }
    if (game.team1_id != undefined){
        let team1Parsed = game.team1_id.split("+");
        let teamId1 = team1Parsed[0].trim();
        let teamRole1 = team1Parsed[1].trim().toLowerCase();
        let avatarImg1 = document.querySelector(".player1-avatar img");
        if(teamRole1 == "x" || teamRole1 == "o"){
            avatarImg1.src = "resources/" + teamRole1 + "_role.png";
        }
        else {
            avatarImg1.src = "resources/player1avatar.png";
        }
        document.getElementById("player1-id").innerText = teamId1;
    }
    else {
        document.getElementById("player1-id").innerText = "";
        let avatarImg1 = document.querySelector(".player1-avatar img");
        avatarImg1.src = "resources/player1avatar.png";
    }

    if (game.team2_id != undefined){
        let team2Parsed = game.team2_id.split("+");
        let teamId2 = team2Parsed[0].trim();
        let teamRole2 = team2Parsed[1].trim().toLowerCase();
        let avatarImg2 = document.querySelector(".player2-avatar img");
        if(teamRole2 == "x" || teamRole2 == "o"){
            avatarImg2.src = "resources/" + teamRole2 + "_role.png";
        }
        else {
            avatarImg2.src = "resources/player2avatar.png";
        }
        document.getElementById("player2-id").innerText = teamId2;
      }
      else {
        document.getElementById("player2-id").innerText = "";
        let avatarImg2 = document.querySelector(".player2-avatar img");
        avatarImg2.src = "resources/player2avatar.png";
      }
    document.getElementById("match-id").innerText = `Match ID: ${game.match_id != undefined ? game.match_id : ""}`
    document.getElementById('player1-time').innerHTML = game.time1 != undefined ? game.time1.toFixed(5) : ""
    document.getElementById('player2-time').innerHTML = game.time2 != undefined ? game.time2.toFixed(5) : ""
    document.getElementById('score1').innerHTML = game.score1 != undefined ? game.score1 : ""
    document.getElementById('score2').innerHTML = game.score2 != undefined ? game.score2 : ""
}