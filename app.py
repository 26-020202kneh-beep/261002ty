```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌 깨기 게임")
st.write("키보드 ← → 로 패들을 움직이세요.")

game = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        background: #111827;
        font-family: Arial, sans-serif;
        color: white;
        text-align: center;
        overflow: hidden;
    }

    #gameContainer {
        width: 100%;
        max-width: 800px;
        margin: auto;
    }

    canvas {
        width: 100%;
        max-width: 760px;
        background: #050816;
        border: 3px solid #ffffff;
        border-radius: 10px;
        display: block;
        margin: 10px auto;
    }

    #info {
        display: flex;
        justify-content: center;
        gap: 30px;
        font-size: 20px;
        font-weight: bold;
        margin: 10px;
    }

    button {
        border: none;
        border-radius: 8px;
        padding: 12px 25px;
        font-size: 17px;
        cursor: pointer;
        background: #2563eb;
        color: white;
    }

    button:hover {
        background: #1d4ed8;
    }

    #message {
        font-size: 24px;
        font-weight: bold;
        min-height: 35px;
    }
</style>
</head>

<body>

<div id="gameContainer">

    <div id="info">
        <div>점수: <span id="score">0</span></div>
        <div>목숨: <span id="lives">3</span></div>
        <div>레벨: <span id="level">1</span></div>
    </div>

    <canvas id="gameCanvas" width="760" height="500"></canvas>

    <div id="message"></div>

    <button onclick="restartGame()">게임 다시 시작</button>

</div>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const livesText = document.getElementById("lives");
const levelText = document.getElementById("level");
const messageText = document.getElementById("message");

// =========================
// 게임 변수
// =========================

let score = 0;
let lives = 3;
let level = 1;

let gameRunning = true;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 70,
    radius: 9,
    dx: 4,
    dy: -4
};

let paddle = {
    width: 120,
    height: 15,
    x: canvas.width / 2 - 60,
    y: canvas.height - 30,
    speed: 8
};

let rightPressed = false;
let leftPressed = false;

// =========================
// 벽돌 설정
// =========================

const brickRowCount = 5;
const brickColumnCount = 9;

const brickWidth = 70;
const brickHeight = 22;

const brickPadding = 10;
const brickOffsetTop = 55;
const brickOffsetLeft = 25;

let bricks = [];

function createBricks() {

    bricks = [];

    for (let c = 0; c < brickColumnCount; c++) {

        bricks[c] = [];

        for (let r = 0; r < brickRowCount; r++) {

            bricks[c][r] = {
                x: 0,
                y: 0,
                status: 1
            };

        }
    }
}

createBricks();

// =========================
// 키보드
// =========================

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {

    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = true;
    }

    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {

    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = false;
    }

    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = false;
    }
}

// =========================
// 공 그리기
// =========================

function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.closePath();
}

// =========================
// 패들 그리기
// =========================

function drawPaddle() {

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.fillStyle = "#3b82f6";
    ctx.fill();

    ctx.closePath();
}

// =========================
// 벽돌 그리기
// =========================

function drawBricks() {

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            if (bricks[c][r].status === 1) {

                const brickX =
                    c * (brickWidth + brickPadding)
                    + brickOffsetLeft;

                const brickY =
                    r * (brickHeight + brickPadding)
                    + brickOffsetTop;

                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;

                ctx.beginPath();

                ctx.roundRect(
                    brickX,
                    brickY,
                    brickWidth,
                    brickHeight,
                    5
                );

                // 줄마다 다른 색
                const colors = [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#8b5cf6"
                ];

                ctx.fillStyle = colors[r % colors.length];

                ctx.fill();

                ctx.closePath();
            }
        }
    }
}

// =========================
// 충돌 검사
// =========================

function collisionDetection() {

    let remaining = 0;

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            const brick = bricks[c][r];

            if (brick.status === 1) {

                remaining++;

                if (
                    ball.x > brick.x &&
                    ball.x < brick.x + brickWidth &&
                    ball.y > brick.y &&
                    ball.y < brick.y + brickHeight
                ) {

                    ball.dy = -ball.dy;

                    brick.status = 0;

                    score += 10;

                    scoreText.textContent = score;
                }
            }
        }
    }

    // 모든 벽돌 제거
    if (remaining === 0) {

        level++;

        levelText.textContent = level;

        createBricks();

        ball.x = canvas.width / 2;
        ball.y = canvas.height - 70;

        ball.dx *= 1.1;
        ball.dy *= 1.1;
    }
}

// =========================
// 게임 업데이트
// =========================

function update() {

    if (!gameRunning) {
        return;
    }

    // 벽 충돌

    if (
        ball.x + ball.dx >
        canvas.width - ball.radius ||

        ball.x + ball.dx <
        ball.radius
    ) {

        ball.dx = -ball.dx;
    }

    if (
        ball.y + ball.dy <
        ball.radius
    ) {

        ball.dy = -ball.dy;
    }

    // 패들 충돌

    if (
        ball.y + ball.dy >
        canvas.height - ball.radius - 25
    ) {

        if (
            ball.x >= paddle.x &&
            ball.x <= paddle.x + paddle.width
        ) {

            ball.dy = -Math.abs(ball.dy);

            // 패들 위치에 따라 공의 방향 변경
            const hitPosition =
                (ball.x - paddle.x) / paddle.width;

            ball.dx =
                (hitPosition - 0.5) * 10;
        }
    }

    // 공이 바닥으로 떨어짐

    if (
        ball.y + ball.dy >
        canvas.height - ball.radius
    ) {

        lives--;

        livesText.textContent = lives;

        if (lives <= 0) {

            gameOver();

            return;
        }

        resetBall();
    }

    // 패들 이동

    if (rightPressed) {

        paddle.x += paddle.speed;

        if (
            paddle.x + paddle.width >
            canvas.width
        ) {
            paddle.x =
                canvas.width - paddle.width;
        }
    }

    if (leftPressed) {

        paddle.x -= paddle.speed;

        if (paddle.x < 0) {
            paddle.x = 0;
        }
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    collisionDetection();
}

// =========================
// 공 초기화
// =========================

function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 70;

    ball.dx =
        Math.random() > 0.5 ? 4 : -4;

    ball.dy = -4;
}

// =========================
// 게임 오버
// =========================

function gameOver() {

    gameRunning = false;

    messageText.textContent =
        "GAME OVER!";

}

// =========================
// 다시 시작
// =========================

function restartGame() {

    score = 0;
    lives = 3;
    level = 1;

    scoreText.textContent = score;
    livesText.textContent = lives;
    levelText.textContent = level;

    messageText.textContent = "";

    paddle.x =
        canvas.width / 2 -
        paddle.width / 2;

    ball.dx = 4;
    ball.dy = -4;

    resetBall();

    createBricks();

    gameRunning = true;
}

// =========================
// 화면 그리기
// =========================

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();

    drawBall();

    drawPaddle();

    update();

    requestAnimationFrame(draw);
}

// 게임 시작
draw();

</script>

</body>
</html>
"""

components.html(
    game,
    height=650,
    scrolling=False
)
```
