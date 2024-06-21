document.addEventListener('DOMContentLoaded', function () {
    let selectedChampions = [];
    let championDict = {};

    let cost1Div = document.getElementById('cost-1');
    let cost2Div = document.getElementById('cost-2');
    let cost3Div = document.getElementById('cost-3');
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
                button.classList.add(`cost-${champion.cost}`);

                let portrait = document.createElement('div');
                portrait.classList.add('champion-portrait');

                let borderDiv = document.createElement('div');
                borderDiv.classList.add('champion-border');

                let imageDiv = document.createElement('div');
                imageDiv.classList.add('champion-image');
                imageDiv.style.backgroundImage = `url('/static/images/champions/cost-${championDict[champion.name].cost}/${champion.name}.jpeg')`;

                portrait.append(borderDiv);
                portrait.append(imageDiv);

                let nameDiv = document.createElement('div');
                nameDiv.classList.add('champion-name');
                nameDiv.innerText = champion.name;

                button.append(portrait);
                button.appendChild(nameDiv);

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
        const index = selectedChampions.findIndex(c => c.name === champion);
        if (index > -1) {
            selectedChampions.splice(index, 1);
        } else {
            if (championDict[champion].cost === 1)
                selectedChampions.push({ name: champion, star: 2 })
            else
                selectedChampions.push({ name: champion, star: 1 });
        }
        updateSelectedChampions();
        updateComps();
    }

    function updateSelectedChampions() {
        selectedChampionsDiv.innerHTML = '';
        selectedChampions.forEach(champion => {
            let button = document.createElement('div');
            button.classList.add(`cost-${championDict[champion.name].cost}`)

            let portrait = document.createElement('div');
            portrait.classList.add('champion-portrait');

            let borderDiv = document.createElement('div');
            borderDiv.classList.add('champion-border');

            let imageDiv = document.createElement('div');
            imageDiv.classList.add('champion-image');
            imageDiv.style.backgroundImage = `url('/static/images/champions/cost-${championDict[champion.name].cost}/${champion.name}.jpeg')`;

            portrait.appendChild(borderDiv);
            portrait.appendChild(imageDiv);

            let nameDiv = document.createElement('div');
            nameDiv.classList.add('champion-name');
            nameDiv.innerText = champion.name;

            let starSelect = document.createElement('select');
            starSelect.classList.add('star-select');
            starSelect.innerHTML = `
                <option value="1" ${champion.star === 1 ? 'selected' : ''}>★</option>
                <option value="2" ${champion.star === 2 ? 'selected' : ''}>★★</option>
                <option value="3" ${champion.star === 3 ? 'selected' : ''}>★★★</option>
            `;
            starSelect.onchange = function (event) {
                event.stopPropagation(); // 이벤트 버블링 방지
                champion.star = parseInt(starSelect.value);
                updateComps();
            };

            button.appendChild(portrait);
            button.appendChild(nameDiv);
            button.appendChild(starSelect);

            button.onclick = function (event) {
                if (event.target.tagName !== 'SELECT') {
                    toggleChampion(champion.name);
                }
            }
            selectedChampionsDiv.appendChild(button);
        });
    }

    function updateComps() {
        fetch('/get_comps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ champions: selectedChampions })
        }).then(response => response.json())
            .then(data => {
                resultsDiv.innerHTML = '';
                data.forEach(item => {
                    let compDiv = document.createElement('div');
                    compDiv.innerText = `${item.score} ${item.comp.name}`;
                    compDiv.classList.add('comp-container')

                    let championPortraits = document.createElement('div');
                    championPortraits.classList.add('champion-portraits');

                    item.comp.champions.forEach(championName => {
                        let PortraitName = document.createElement('div');

                        let portrait = document.createElement('div');
                        portrait.classList.add('champion-portrait');

                        let borderDiv = document.createElement('div');
                        borderDiv.classList.add('champion-border');
                        borderDiv.classList.add(`cost-${championDict[championName].cost}`);

                        let imageDiv = document.createElement('div');
                        imageDiv.classList.add('champion-image');
                        imageDiv.style.backgroundImage = `url('/static/images/champions/cost-${championDict[championName].cost}/${championName}.jpeg')`;

                        portrait.appendChild(borderDiv);
                        portrait.appendChild(imageDiv);

                        let nameDiv = document.createElement('div');
                        nameDiv.classList.add('champion-name');
                        nameDiv.innerText = championName;

                        PortraitName.appendChild(portrait);
                        PortraitName.appendChild(nameDiv);

                        championPortraits.appendChild(PortraitName);
                    });

                    compDiv.appendChild(championPortraits);
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
