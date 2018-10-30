const cardNumberInput = document.getElementById('card-number-input');


cardNumberInput.addEventListener('keyup', function() {
  let tmpValue = this.value.split(' ').join('');

  let newValue;
  if (tmpValue.length < 2) {
    newValue = tmpValue;
  } else if (2 <= tmpValue.length && tmpValue.length < 8) {
    newValue = [
      tmpValue.slice(0, 1),
      tmpValue.slice(1)
    ].join(' ');
  } else {
    newValue = [
      tmpValue.slice(0, 1),
      tmpValue.slice(1, 7),
      tmpValue.slice(7)
    ].join(' ');
  }

  this.value = newValue;
});
