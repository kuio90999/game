// 游戏状态
const gameState = {
    currentScreen: 'main-menu',
    roomCode: null,
    playerName: null,
    isPlayer1: false
};

// API调用函数
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    return await response.json();
}

// 切换屏幕
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    gameState.currentScreen = screenId;
}

// 显示结果
function showResult(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `result ${type}`;
}

// 清除结果
function clearResult(elementId) {
    const element = document.getElementById(elementId);
    element.textContent = '';
    element.className = 'result';
}

// 创建房间
async function createRoom() {
    const playerName = document.getElementById('create-name').value.trim();
    
    if (!playerName) {
        showResult('create-result', '请输入你的名字！', 'error');
        return;
    }
    
    try {
        const result = await apiCall('/api/create', 'POST', { player: playerName });
        
        if (result.error) {
            showResult('create-result', result.error, 'error');
            return;
        }
        
        gameState.roomCode = result.room_code;
        gameState.playerName = playerName;
        gameState.isPlayer1 = true;
        
        showResult('create-result', `房间创建成功！房间码：${result.room_code}，正在进入游戏...`, 'success');
        
        // 延迟进入游戏界面
        setTimeout(() => {
            enterGame();
        }, 1500);
        
    } catch (error) {
        showResult('create-result', '创建房间失败，请重试！', 'error');
    }
}

// 加入房间
async function joinRoom() {
    const playerName = document.getElementById('join-name').value.trim();
    const roomCode = document.getElementById('join-code').value.trim().toUpperCase();
    
    if (!playerName) {
        showResult('join-result', '请输入你的名字！', 'error');
        return;
    }
    
    if (!roomCode) {
        showResult('join-result', '请输入房间码！', 'error');
        return;
    }
    
    try {
        const result = await apiCall('/api/join', 'POST', { 
            room_code: roomCode, 
            player: playerName 
        });
        
        if (result.error) {
            showResult('join-result', result.error, 'error');
            return;
        }
        
        gameState.roomCode = roomCode;
        gameState.playerName = playerName;
        gameState.isPlayer1 = false;
        
        showResult('join-result', `成功加入房间！玩家1：${result.player1}，玩家2：${playerName}`, 'success');
        
        // 延迟进入游戏界面
        setTimeout(() => {
            enterGame();
        }, 1500);
        
    } catch (error) {
        showResult('join-result', '加入房间失败，请重试！', 'error');
    }
}

// 进入游戏界面
function enterGame() {
    document.getElementById('game-room-code').textContent = gameState.roomCode;
    document.getElementById('game-player-name').textContent = gameState.playerName;
    
    // 清空游戏界面
    document.getElementById('game-result').innerHTML = '';
    document.getElementById('game-result').className = 'game-result';
    document.getElementById('guess-list').innerHTML = '';
    document.getElementById('guess-input').value = '';
    
    showScreen('game-screen');
    
    // 加载房间信息
    loadRoomInfo();
}

// 加载房间信息
async function loadRoomInfo() {
    try {
        const room = await apiCall(`/api/room/${gameState.roomCode}`);
        
        if (room.error) {
            alert(room.error);
            return;
        }
        
        // 显示猜测记录
        if (room.guesses && room.guesses.length > 0) {
            displayGuessHistory(room.guesses);
        }
        
    } catch (error) {
        console.error('加载房间信息失败:', error);
    }
}

// 显示猜测历史
function displayGuessHistory(guesses) {
    const guessList = document.getElementById('guess-list');
    guessList.innerHTML = '';
    
    guesses.forEach((guess, index) => {
        const guessItem = document.createElement('div');
        guessItem.className = 'guess-item';
        guessItem.innerHTML = `
            <div class="guess-name">${guess.surname}${guess.name}</div>
            <div class="guess-hints">
                <span class="guess-hint diff">#${index + 1}</span>
            </div>
        `;
        guessList.appendChild(guessItem);
    });
    
    // 滚动到底部
    guessList.scrollTop = guessList.scrollHeight;
}

// 猜测人物
async function makeGuess() {
    const characterName = document.getElementById('guess-input').value.trim();
    
    if (!characterName) {
        alert('请输入人物名字！');
        return;
    }
    
    try {
        const result = await apiCall('/api/guess', 'POST', {
            room_code: gameState.roomCode,
            player: gameState.playerName,
            character_name: characterName
        });
        
        if (result.error) {
            return;
        }
        
        // 显示结果
        displayGuessResult(characterName, result);
        
        // 清空输入框
        document.getElementById('guess-input').value = '';
        
        // 如果猜对了，显示成功信息
        if (result.correct) {
            setTimeout(() => {
                alert(`恭喜你猜对了！答案就是【${result.answer.surname}${result.answer.name}】！`);
            }, 500);
        }
        
    } catch (error) {
        console.error('猜测失败:', error);
    }
}

// 显示猜测结果
function displayGuessResult(characterName, result) {
    const gameResult = document.getElementById('game-result');
    
    if (result.correct) {
        gameResult.className = 'game-result show correct';
        gameResult.innerHTML = `
            <div class="result-title">恭喜你猜对了！</div>
            <div>答案就是【${result.answer.surname}${result.answer.name}】！</div>
        `;
    } else {
        gameResult.className = 'game-result show wrong';
        
        let hintsHtml = '<div class="result-title">猜错了！提示：</div>';
        hintsHtml += '<ul class="hints-list">';
        
        result.hints.forEach(hint => {
            let statusClass = 'diff';
            if (hint.status.includes('一致') || hint.status.includes('相同')) {
                statusClass = 'same';
            } else if (hint.status.includes('有相同的字')) {
                statusClass = 'special';
            }
            
            hintsHtml += `
                <li>
                    <span class="hint-attr">${hint.attr}：</span>
                    <span class="hint-value">${hint.value || ''}</span>
                    <span class="hint-status ${statusClass}">${hint.status}</span>
                </li>
            `;
        });
        
        hintsHtml += '</ul>';
        
        // 添加总结信息
        if (result.summary && result.summary.length > 0) {
            hintsHtml += '<div class="summary-section">';
            hintsHtml += '<div class="summary-title">当前限定范围：</div>';
            hintsHtml += '<ul class="summary-list">';
            
            result.summary.forEach(item => {
                hintsHtml += `<li>${item}</li>`;
            });
            
            hintsHtml += '</ul>';
            hintsHtml += '</div>';
        }
        
        gameResult.innerHTML = hintsHtml;
    }
    
    // 添加到猜测记录
    addGuessToList(characterName, result);
}

// 事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 主菜单按钮
    document.getElementById('btn-create').addEventListener('click', () => {
        showScreen('create-screen');
    });
    
    document.getElementById('btn-join').addEventListener('click', () => {
        showScreen('join-screen');
    });
    
    // 创建房间界面
    document.getElementById('btn-create-confirm').addEventListener('click', createRoom);
    document.getElementById('btn-create-back').addEventListener('click', () => {
        showScreen('main-menu');
        clearResult('create-result');
    });
    
    // 加入房间界面
    document.getElementById('btn-join-confirm').addEventListener('click', joinRoom);
    document.getElementById('btn-join-back').addEventListener('click', () => {
        showScreen('main-menu');
        clearResult('join-result');
    });
    
    // 游戏界面
    document.getElementById('btn-guess').addEventListener('click', makeGuess);
    document.getElementById('guess-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            makeGuess();
        }
    });
    
    document.getElementById('btn-game-back').addEventListener('click', () => {
        if (confirm('确定要退出游戏吗？')) {
            showScreen('main-menu');
            gameState.roomCode = null;
            gameState.playerName = null;
        }
    });
});
