const startRollBtn = document.querySelector('#startRollBtn');
const stopRollBtn = document.querySelector('#stopRollBtn');
const scoringOptionBtn = document.querySelector('#scoringOptionBtn')
const rollResult = document.querySelector('.rollResult');

const diceImg1 = document.createElement('img');
const diceImg2 = document.createElement('img');
const diceImg3 = document.createElement('img');
const diceImg4 = document.createElement('img');
const diceImg5 = document.createElement('img');

rollResult.appendChild(diceImg1);
rollResult.appendChild(diceImg2);
rollResult.appendChild(diceImg3);
rollResult.appendChild(diceImg4);
rollResult.appendChild(diceImg5);

let diceBlob1 = fetchAndDecode('/static/dice/Dice1.svg');
let diceBlob2 = fetchAndDecode('/static/dice/Dice2.svg');
let diceBlob3 = fetchAndDecode('/static/dice/Dice3.svg');
let diceBlob4 = fetchAndDecode('/static/dice/Dice4.svg');
let diceBlob5 = fetchAndDecode('/static/dice/Dice5.svg');
let diceBlob6 = fetchAndDecode('/static/dice/Dice6.svg');

let rAF;
let rollCount = 1;

diceImg1.setAttribute('id', 'diceImg1');
diceImg2.setAttribute('id', 'diceImg2');
diceImg3.setAttribute('id', 'diceImg3');
diceImg4.setAttribute('id', 'diceImg4');
diceImg5.setAttribute('id', 'diceImg5');
diceImg1.setAttribute('class', 'unselected');
diceImg2.setAttribute('class', 'unselected');
diceImg3.setAttribute('class', 'unselected');
diceImg4.setAttribute('class', 'unselected');
diceImg5.setAttribute('class', 'unselected');
diceImg1.setAttribute('data-id', 'die');
diceImg2.setAttribute('data-id', 'die');
diceImg3.setAttribute('data-id', 'die');
diceImg4.setAttribute('data-id', 'die');
diceImg5.setAttribute('data-id', 'die');

startRollBtn.addEventListener('click', startRoll);
stopRollBtn.addEventListener('click', stopRoll);
scoringOptionBtn.addEventListener('click', selectScoringOption)

console.log('PICK THAT OPTION');
let diceImgArray = [diceImg1, diceImg2, diceImg3, diceImg4, diceImg5];

function startRoll() {
  if(rollCount < 4) {
    stopRollBtn.style.display = 'block';
    startRollBtn.style.display = 'none';

    // add margin to top of rollResult dice div when added to block
    rollResult.className = "mt-3";

    // fetch all dice blobs, and get objectURLs
    Promise.all([diceBlob1, diceBlob2, diceBlob3, diceBlob4, diceBlob5, diceBlob6]).then(values => {
        let dice1ObjectURL = URL.createObjectURL(values[0]);
        let dice2ObjectURL = URL.createObjectURL(values[1]);
        let dice3ObjectURL = URL.createObjectURL(values[2]);
        let dice4ObjectURL = URL.createObjectURL(values[3]);
        let dice5ObjectURL = URL.createObjectURL(values[4]);
        let dice6ObjectURL = URL.createObjectURL(values[5]);

        // create array for randomly selecting dice images from
        let diceObjectURLArray = [
          dice1ObjectURL,
          dice2ObjectURL,
          dice3ObjectURL,
          dice4ObjectURL,
          dice5ObjectURL,
          dice6ObjectURL
        ]

        // main dice rolling animation using rAF
        let rollAction = function() {
          for(i = 0; i < 5; i++) {
            if(diceImgArray[i].getAttribute('class') === 'unselected') {
              diceImgArray[i].setAttribute('src', diceObjectURLArray[random(6)]);
            }
          }

          rAF = requestAnimationFrame(rollAction);
        }

        rollAction();
        rollCount++;
    });
  }
};

function stopRoll() {
  if (rollCount === 2) {
    stopRollHandler();

    startRollBtn.textContent = 'Roll Two';
    startRollBtn.style.display = 'block';
  } else if (rollCount === 3) {
    stopRollHandler();

    startRollBtn.textContent = 'Roll Three';
    startRollBtn.style.display = 'block';
  } else {
    for(let i = 0; i < 5; i++) {
      diceImgArray[i].setAttribute('class', 'selected')
    }
    stopRollBtn.style.display = 'none'
    scoringOptionBtn.style.display = 'block';
  }
}

function stopRollHandler() {
  stopRollBtn.style.display = 'none';

  cancelAnimationFrame(rAF);

  diceImg1.addEventListener('click', toggleDice);
  diceImg2.addEventListener('click', toggleDice);
  diceImg3.addEventListener('click', toggleDice);
  diceImg4.addEventListener('click', toggleDice);
  diceImg5.addEventListener('click', toggleDice);
}


function toggleDice(e) {
  if(e.target.getAttribute('class') === 'unselected') {
    e.target.className = 'selected';
  } else {
    e.target.className = 'unselected';
  }
}

function selectScoringOption() {
  console.log('PICK THAT OPTION');
}

function fetchAndDecode(url) {
  return fetch(url).then(response => {
    if(!response.ok) {
      throw new Error('HTTP error! status: ${response.status}');
    } else {
      return response.blob();
    }
  })
  .catch(e => {
    console.log('There has been a problem with your fetch operation for resource "${url}": ' + e.message);
  });
}

function random(number) {
  return Math.floor(Math.random() * number);
}
