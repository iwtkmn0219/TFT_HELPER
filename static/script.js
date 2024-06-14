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
                toggleChampion(champion.name);
            };
            championSelectionDiv.appendChild(button);
        });
    });

    function toggleChampion(champion) {
        const index = selectedChampions.indexOf(champion);
        if (index > -1) {
            selectedChampions.splice(index, 1);
        } else {
            selectedChampions.push(champion)
        }
        updateSelectedChampions();
        updateComps();
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
                data.forEach(item => {
                    let compDiv = document.createElement('div');
                    compDiv.innerText = `${item.score} 조합 이름: ${item.comp.name}, 챔피언: ${item.comp.champions.join(', ')}`;
                    resultsDiv.appendChild(compDiv);
                });
            });
    }
});
