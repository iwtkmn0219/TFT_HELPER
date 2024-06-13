document.addEventListener('DOMContentLoaded', function () {
    let champions = ["가렌", "잭스", "시비르", "리븐", "자이라", "조이"];
    let selectedChampions = [];

    let championSelectionDiv = document.getElementById('champion-selection');
    let selectedChampionsDiv = document.getElementById('selected-champions');
    let resultsDiv = document.getElementById('results');

    champions.forEach(champion => {
        let button = document.createElement('button');
        button.innerText = champion;
        button.onclick = function () {
            addChampion(champion);
        };
        championSelectionDiv.appendChild(button);
    });

    function addChampion(champion) {
        if (!selectedChampions.includes(champion)) {
            selectedChampions.push(champion);
            updateSelectedChampions();
            updateCombinations();
        }
    }

    function updateSelectedChampions() {
        selectedChampionsDiv.innerHTML = selectedChampions.join(', ');
    }

    function updateCombinations() {
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
