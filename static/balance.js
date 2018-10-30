const balanceWrapper = document.getElementById('balance-wrapper');
const cardBalance = document.getElementById('card-balance');
const cardNumber = document.getElementById('card-number');
const loader = document.getElementById('loader');


function check_balance() {
  let urlParams = new URLSearchParams(window.location.search);
  let card_number = urlParams.get('card_number').split(' ').join('');

  fetch('/query/?card_number=' + card_number)
    .then(function(response) {
      return response.json();
    })
    .then(function (card_info) {
      cardBalance.innerText = card_info['card_balance'];
      cardNumber.innerText = card_info['card_number'];

      loader.style.display = 'none';
      balanceWrapper.style.display = 'grid';
    });
}

document.addEventListener('DOMContentLoaded', check_balance);
