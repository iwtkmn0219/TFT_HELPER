document.addEventListener('DOMContentLoaded', function () {
    loadChampionList();
    loadCompList();
});

function loadChampionList() {
    fetch('/get_champion_list')
        .then(response => response.json())
        .then(champions => {
            const championListDiv = document.getElementById('champion-list');
            champions.forEach(champion => {
                const championItem = document.createElement('div');
                championItem.classList.add('champion-item');
                championItem.innerHTML = `
                    <span>${champion.name}</span>
                    <input type="text" value="${champion.value[0]}" data-champion="${champion.name}" data-index="0">
                    <input type="text" value="${champion.value[1]}" data-champion="${champion.name}" data-index="1">
                    <input type="text" value="${champion.value[2]}" data-champion="${champion.name}" data-index="2">
                `;
                championListDiv.appendChild(championItem);
            });
        });
}

function saveChampionsValues() {
    const inputs = document.querySelectorAll('#champion-list input');
    const championValues = {}

    inputs.forEach(input => {
        const name = input.getAttribute('data-champion');
        const index = parseInt(input.getAttribute('data-index'));
        const value = input.value;

        if (!championValues[name]) {
            championValues[name] = [];
        }
        championValues[name][index] = value;
    });

    const championValuesArray = Object.keys(championValues).map(name => ({
        name: name,
        value: championValues[name]
    }));

    fetch('/update_champion_values', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(championValuesArray)
    }).then(response => response.json())
        .then(data => {
            alert('챔피언 밸류가 업데이트되었습니다.');
        });
}

function loadCompList() {
    fetch('/get_comp_list')
        .then(response => response.json())
        .then(comps => {
            const compListDiv = document.getElementById('comp-list');
            comps.forEach(comp => {
                const compItem = document.createElement('div');
                compItem.classList.add('comp-item');
                compItem.innerHTML = `
                    <span>${comp.name}</span>
                    <input type="text" value="${comp.champions.join(', ')}" data-comp="${comp.name}">
                    <button onclick="deleteComp('${comp.name}')">삭제</button>
                    <button onclick="updateComp('${comp.name}')">수정</button>
                `;
                compListDiv.appendChild(compItem);
            });
        });
}

function createNewComp() {
    const newCompName = prompt('새 조합 이름을 입력하세요:');
    if (newCompName) {
        // 새로운 조합 추가 로직
    }
}

function deleteComp(compName) {
    fetch(`/delete_comp/${compName}`, {
        method: 'DELETE'
    }).then(response => response.json())
        .then(data => {
            alert('조합이 삭제되었습니다.');
            loadCompList();
        });
}

function updateComp(compName) {
    const newChampions = prompt('새로운 챔피언들을 입력하세요 (콤마로 구분):');
    if (newChampions) {
        fetch('/update_comp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: compName,
                champions: newChampions.split(',').map(c => c.trim())
            })
        }).then(response => response.json())
            .then(data => {
                alert('조합이 수정되었습니다.');
                loadCompList();
            });
    }
}