document.addEventListener('DOMContentLoaded', function () {
    let selectedChampions = [];

    let championSelectionDiv = document.getElementById('champion-selection');
    let selectedChampionsDiv = document.getElementById('selected-champions');
    let resultsDiv = document.getElementById('results');

    // 챔피언 목록을 서버에서 불러오기
    fetch('/get_champion_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(champions => {
        champions.forEach(champion => {
            let button = document.createElement('button');
            button.innerText = champion.name;
            button.onclick = function () {
                addChampion(champion.name);
            };
            championSelectionDiv.appendChild(button);
        });
    });

    function addChampion(champion) {
        if (!selectedChampions.includes(champion)) {
            selectedChampions.push(champion);
            updateSelectedChampions();
            updateComps();
        }
    }

    function updateSelectedChampions() {
        selectedChampionsDiv.innerHTML = selectedChampions.join(', ');
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
                data.forEach(comp => {
                    let compDiv = document.createElement('div');
                    compDiv.innerText = `조합 이름: ${comp.name}, 챔피언: ${comp.champions.join(', ')}`;
                    resultsDiv.appendChild(compDiv);
                });
            });
    }
});
