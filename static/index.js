document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
    var butt = document.querySelectorAll('.thing');

    for (let i = 0; i < butt.length; i++) {
      butt[i].disabled = true;
    };

    document.querySelectorAll('.thing').forEach(button => {
      button.onclick = () => {
        const move = button.dataset.move;
        socket.emit('input move', {'move': move});
      };
    });

    document.getElementById('train').onclick = () => {
      document.getElementById('message').innerHTML = "training..."
    };
  });


  document.getElementById('start').onclick = () => {
    var butt = document.querySelectorAll('.thing');

    for (let i = 0; i < butt.length; i++) {
      butt[i].disabled = false;
    };

    document.getElementById('start').disabled = true;
    socket.emit('start');
  };


  var slider = document.getElementById('range')
  slider.oninput = () => {
    document.getElementById('number').value = slider.value;
  };

  var textbox = document.getElementById('number')
  textbox.oninput = () => {
    slider.value = textbox.value;
  }


  socket.on('new state', (board, message) => {
    var butt = document.querySelectorAll('.thing');

    if (message != 'cont'){
      for (let i = 0; i < butt.length; i++) {
        butt[i].disabled = true;
      };

      document.getElementById('message').innerHTML = message;
    };

    document.getElementById('0').innerHTML = board[0][0];
    document.getElementById('1').innerHTML = board[0][1];
    document.getElementById('2').innerHTML = board[0][2];
    document.getElementById('3').innerHTML = board[1][0];
    document.getElementById('4').innerHTML = board[1][1];
    document.getElementById('5').innerHTML = board[1][2];
    document.getElementById('6').innerHTML = board[2][0];
    document.getElementById('7').innerHTML = board[2][1];
    document.getElementById('8').innerHTML = board[2][2];
  });


  socket.on('invalid', () => {
    alert("Invalid Move");
  });

});
