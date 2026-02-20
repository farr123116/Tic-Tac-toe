let board = ["","","","","","","","",""];
let turn = "X";
let finished = false;

const boardDiv = document.getElementById("board");
const status = document.getElementById("status");

function drawBoard(){
    boardDiv.innerHTML = "";

    board.forEach((val,i)=>{
        let btn = document.createElement("button");
        btn.className="cell";
        btn.textContent = val;
        btn.onclick = ()=>move(i);
        boardDiv.appendChild(btn);
    });

    status.textContent = turn + " turn";
}

function move(i){
    if(board[i]!=="" || finished) return;

    board[i]=turn;

    if(checkWinner()){
        status.textContent = turn + " wins!";
        finished=true;
        drawBoard();
        return;
    }

    if(board.every(c=>c!=="")){
        status.textContent="Draw!";
        finished=true;
        drawBoard();
        return;
    }

    turn = turn==="X"?"O":"X";
    drawBoard();
}

function checkWinner(){
    const wins=[
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ];
    return wins.some(([a,b,c]) =>
        board[a] && board[a]===board[b] && board[a]===board[c]
    );
}

function resetGame(){
    board=["","","","","","","","",""];
    turn="X";
    finished=false;
    drawBoard();
}

drawBoard();
