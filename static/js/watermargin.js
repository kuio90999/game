// 游戏状态
const gameState = {
    characters: [],
    currentAnswer: null,
    guessCount: 0,
    shownHints: []
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

// 加载人物列表
async function loadCharacters() {
    try {
        const characters = await apiCall('/api/watermargin/characters');
        if (characters && !characters.error) {
            gameState.characters = characters;
        }
    } catch (error) {
        console.error('加载人物列表失败:', error);
    }
}

// 开始新游戏
async function startNewGame() {
    try {
        const result = await apiCall('/api/watermargin/new-game', 'POST');
        if (result && !result.error) {
            gameState.currentAnswer = result.answer;
            gameState.guessCount = 0;
            gameState.shownHints = [];
            
            // 显示初始提示
            let hintHtml = '<div class="hint-box">';
            if (result.initial_hints) {
                result.initial_hints.forEach(hint => {
                    hintHtml += `<span>${hint.label}：${hint.value}</span>`;
                    gameState.shownHints.push(hint.type);
                });
            }
            hintHtml += '</div>';
            document.getElementById('initial-hint').innerHTML = hintHtml;
            
            // 显示提示按钮
            document.getElementById('btn-hint').style.display = 'inline-block';
            
            // 重置界面
            document.getElementById('game-result').innerHTML = '';
            document.getElementById('game-result').className = 'game-result';
            document.getElementById('guess-list').innerHTML = '';
            document.getElementById('guess-input').value = '';
            
            // 重新启用输入框和按钮
            document.getElementById('guess-input').disabled = false;
            document.getElementById('btn-guess').disabled = false;
            document.getElementById('guess-input').style.opacity = '1';
            document.getElementById('btn-guess').style.opacity = '1';
            
            // 移除新游戏按钮
            const newGameSection = document.querySelector('.new-game-section');
            if (newGameSection) {
                newGameSection.remove();
            }
        }
    } catch (error) {
        console.error('开始新游戏失败:', error);
    }
}

// 获取额外提示
async function getHint() {
    try {
        const result = await apiCall('/api/watermargin/get-hint', 'POST');
        if (result && !result.error) {
            // 添加到提示区域
            const hintBox = document.querySelector('.hint-box');
            if (hintBox) {
                const hintSpan = document.createElement('span');
                hintSpan.textContent = `${result.hint.label}：${result.hint.value}`;
                hintBox.appendChild(hintSpan);
            }
            
            gameState.shownHints.push(result.hint.type);
            
            // 如果没有更多提示，隐藏按钮
            if (result.remaining_hints === 0) {
                document.getElementById('btn-hint').style.display = 'none';
            }
        }
    } catch (error) {
        console.error('获取提示失败:', error);
    }
}

// 模糊搜索人物
function searchCharacters(query) {
    if (!query || query.length === 0) {
        return [];
    }
    
    query = query.toLowerCase();
    return gameState.characters.filter(char => {
        const fullName = char.surname + char.name;
        const nickname = char.nickname || '';
        return fullName.toLowerCase().includes(query) || nickname.toLowerCase().includes(query);
    }).slice(0, 10);
}

// 显示下拉框
function showAutocomplete() {
    const input = document.getElementById('guess-input');
    const list = document.getElementById('autocomplete-list');
    const query = input.value.trim();
    
    if (query.length === 0) {
        list.style.display = 'none';
        return;
    }
    
    const results = searchCharacters(query);
    
    if (results.length === 0) {
        list.style.display = 'none';
        return;
    }
    
    list.innerHTML = '';
    results.forEach(char => {
        const fullName = char.surname + char.name;
        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.textContent = `${fullName}（${char.nickname}）`;
        item.addEventListener('click', () => {
            input.value = fullName;
            list.style.display = 'none';
            input.focus();
        });
        list.appendChild(item);
    });
    
    list.style.display = 'block';
}

// 隐藏下拉框
function hideAutocomplete() {
    setTimeout(() => {
        document.getElementById('autocomplete-list').style.display = 'none';
    }, 200);
}

// 猜测人物
async function makeGuess() {
    const characterName = document.getElementById('guess-input').value.trim();
    
    if (!characterName) {
        return;
    }
    
    try {
        const result = await apiCall('/api/watermargin/guess', 'POST', {
            character_name: characterName
        });
        
        if (result.error) {
            return;
        }
        
        gameState.guessCount++;
        
        // 显示结果
        displayGuessResult(characterName, result);
        
        // 清空输入框
        document.getElementById('guess-input').value = '';
        
    } catch (error) {
        console.error('猜测失败:', error);
    }
}

// 显示猜测结果
function displayGuessResult(characterName, result) {
    const gameResult = document.getElementById('game-result');
    
    if (result.correct) {
        const answer = result.answer;
        gameResult.className = 'game-result show correct';
        gameResult.innerHTML = `
            <div class="result-title">恭喜你猜对了！</div>
            <div>答案就是【${answer.surname}${answer.name}】（${answer.nickname}）！</div>
            <div>你用了 ${gameState.guessCount} 次猜对</div>
        `;
        
        // 隐藏输入框和猜测按钮
        document.getElementById('guess-input').disabled = true;
        document.getElementById('btn-guess').disabled = true;
        document.getElementById('guess-input').style.opacity = '0.5';
        document.getElementById('btn-guess').style.opacity = '0.5';
        
        // 显示新游戏按钮
        const newGameSection = document.createElement('div');
        newGameSection.className = 'new-game-section';
        newGameSection.innerHTML = '<button class="btn btn-success" onclick="startNewGame()">等等..再来一个回合！</button>';
        gameResult.parentNode.insertBefore(newGameSection, gameResult.nextSibling);
        
    } else {
        gameResult.className = 'game-result show wrong';
        
        let hintsHtml = '<div class="result-title">猜错了！提示：</div>';
        hintsHtml += '<ul class="hints-list">';
        
        result.hints.forEach(hint => {
            let statusClass = 'diff';
            if (hint.status.includes('一致') || hint.status.includes('相同')) {
                statusClass = 'same';
            } else if (hint.status.includes('更前') || hint.status.includes('更后')) {
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
        
        gameResult.innerHTML = hintsHtml;
    }
    
    // 添加到猜测记录
    addGuessToList(characterName, result);
}

// 添加猜测到列表
function addGuessToList(characterName, result) {
    const guessList = document.getElementById('guess-list');
    
    const guessItem = document.createElement('div');
    guessItem.className = `guess-item ${result.correct ? 'correct' : ''}`;
    
    let hintsHtml = '';
    if (!result.correct && result.hints) {
        hintsHtml = '<div class="guess-hints">';
        result.hints.forEach(hint => {
            let hintClass = 'diff';
            if (hint.status.includes('一致') || hint.status.includes('相同')) {
                hintClass = 'same';
            }
            
            hintsHtml += `<span class="guess-hint ${hintClass}">${hint.attr}: ${hint.status}</span>`;
        });
        hintsHtml += '</div>';
    }
    
    guessItem.innerHTML = `
        <div class="guess-name">#${gameState.guessCount} ${characterName} ${result.correct ? '✓' : ''}</div>
        ${hintsHtml}
    `;
    
    guessList.appendChild(guessItem);
    
    // 滚动到底部
    guessList.scrollTop = guessList.scrollHeight;
}

// 事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 加载人物列表
    loadCharacters();
    
    // 开始新游戏
    startNewGame();
    
    // 猜测按钮
    document.getElementById('btn-guess').addEventListener('click', makeGuess);
    
    // 输入框事件
    const guessInput = document.getElementById('guess-input');
    guessInput.addEventListener('input', showAutocomplete);
    guessInput.addEventListener('focus', showAutocomplete);
    guessInput.addEventListener('blur', hideAutocomplete);
    guessInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const list = document.getElementById('autocomplete-list');
            list.style.display = 'none';
            makeGuess();
        }
    });
    
    // 点击页面其他地方时隐藏下拉框
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.autocomplete-wrapper')) {
            document.getElementById('autocomplete-list').style.display = 'none';
        }
    });
});
