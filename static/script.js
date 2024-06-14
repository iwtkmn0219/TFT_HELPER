document.addEventListener('DOMContentLoaded', function () {
    let selectedChampions = [];
    let championDict = {};

    let cost1Div = document.getElementById('cost-1');
    let cost2Div = document.getElementById('cost-2');
    let cost3Div = document.getElementById('cost-3');
    // let championSelectionDiv = document.getElementById('champion-selection');
    let selectedChampionsDiv = document.getElementById('selected-champions');
    let resultsDiv = document.getElementById('results');
    let resetButton = document.getElementById('reset-button');

    // 챔피언 목록을 서버에서 불러오기
    fetch('/get_champion_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(champions => {
            champions.forEach(champion => {
                championDict[champion.name] = champion;

                let button = document.createElement('div');
                button.innerText = champion.name;
                button.classList.add(`cost-${champion.cost}`)
                button.onclick = function () {
                    toggleChampion(champion.name);
                };
                if (champion.cost === 1) {
                    cost1Div.appendChild(button);
                } else if (champion.cost === 2) {
                    cost2Div.appendChild(button);
                } else if (champion.cost === 3) {
                    cost3Div.appendChild(button);
                }
            });
        });

    function toggleChampion(champion) {
        const index = selectedChampions.indexOf(champion);
        if (index > -1) {
            selectedChampions.splice(index, 1);
        } else {
            selectedChampions.push(champion);
        }
        updateSelectedChampions();
        updateComps();
    }

    function updateSelectedChampions() {
        selectedChampionsDiv.innerHTML = '';
        selectedChampions.forEach(champion => {
            let hex = document.createElement('div');
            hex.innerText = champion;
            hex.classList.add(`cost-${championDict[champion].cost}`)
            hex.onclick = function () {
                toggleChampion(champion);
            }
            selectedChampionsDiv.appendChild(hex);
        });
    }

    function updateComps() {
        fetch('/get_comps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ champions: selectedChampions })
        })
            .then(response => response.json())
            .then(data => {
                resultsDiv.innerHTML = '';
                data.forEach(item => {
                    let compDiv = document.createElement('div');
                    compDiv.innerText = `${item.score} 조합 이름: ${item.comp.name}, 챔피언: ${item.comp.champions.join(', ')}`;
                    resultsDiv.appendChild(compDiv);
                });
            });
    }

    resetButton.onclick = function () {
        selectedChampions = [];
        updateSelectedChampions();
        updateComps();
    }
});
