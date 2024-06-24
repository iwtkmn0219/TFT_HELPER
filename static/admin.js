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
            loadNewCompChampionList(champions);
        });
}

function loadNewCompChampionList(champions) {
    const newCompChampionsDiv = document.getElementById('new-comp-champions');
    champions.forEach(champion => {
        const championItem = document.createElement('div');
        championItem.classList.add('champion-item');
        championItem.innerHTML = `
            <span>${champion.name}</span>
            <button onclick="toggleChampionSelection('${champion.name}')">추가</button>
        `;
        newCompChampionsDiv.appendChild(championItem);
    });
}

let selectedNewCompChampions = [];

function toggleChampionSelection(championName) {
    const index = selectedNewCompChampions.indexOf(championName);
    if (index > -1) {
        selectedNewCompChampions.splice(index, 1);
    } else {
        selectedNewCompChampions.push(championName);
    }
    updateSelectedNewCompChampions();
}

function updateSelectedNewCompChampions() {
    const selectedDiv = document.getElementById('new-comp-champions-selected');
    selectedDiv.innerHTML = '';
    selectedNewCompChampions.forEach(championName => {
        const div = document.createElement('div');
        div.innerText = championName;
        selectedDiv.appendChild(div);
    });
}

function saveNewComp() {
    const compName = document.getElementById('new-comp-name').value;
    if (compName && selectedNewCompChampions.length > 0) {
        fetch('/add_comp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: compName,
                champions: selectedNewCompChampions
            })
        }).then(response => response.json())
            .then(data => {
                alert('새 조합이 추가되었습니다.');
                window.location.reload(); // 페이지 새로고침
            });
    } else {
        alert('조합 이름과 챔피언을 선택해주세요.');
    }
}

function createNewComp() {
    document.getElementById('new-comp-section').style.display = 'block';
}

function cancelNewComp() {
    document.getElementById('new-comp-section').style.display = 'none';
    selectedNewCompChampions = [];
    updateSelectedNewCompChampions();
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
            window.location.reload();
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

function deleteComp(compName) {
    fetch(`/delete_comp/${compName}`, {
        method: 'DELETE'
    }).then(response => response.json())
        .then(data => {
            alert('조합이 삭제되었습니다.');
            window.location.reload();
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