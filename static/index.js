document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  var slider = document.getElementById('range');
  var textbox = document.getElementById('number');
  var button = document.getElementById('train');
  var val = document.querySelectorAll('.values');
  var app = document.getElementById('mybutton');
  button.disabled = true;


  slider.oninput = () => {
    textbox.value = slider.value;

    if (slider.value > 0)
      button.disabled = false;

    else
      button.disabled = true;
  }


  textbox.onkeyup = () => {
    slider.value = textbox.value;

    if (textbox.value <= 0){
      button.disabled = true;
      slider.value = 0;
    }

    else
      button.disabled = false;
  }


  for (let i = 0; i < val.length; i++) {

    val[i].onkeyup = () => {

        if (val[1].value.length == 0 || val[0].value.length == 0){
          app.disabled = true;
        }

        else
          app.disabled = false;
    }
  }


  document.getElementById('start').onclick = () => {
    var butt = document.querySelectorAll('.thing');

    for (let i = 0; i < butt.length; i++) {
      butt[i].disabled = false;
    }

    document.getElementById('start').disabled = true;
    socket.emit('start');
  }


  socket.on('connect', () => {
    var butt = document.querySelectorAll('.thing');

    for (let i = 0; i < butt.length; i++) {
      butt[i].disabled = true;
    }

    document.querySelectorAll('.thing').forEach(button => {
      button.onclick = () => {
        const move = button.dataset.move;
        socket.emit('input move', {'move': move});
      }
    })

    document.getElementById('train').onclick = () => {

      document.getElementById('message').innerHTML = "training...";
    }

    app.onclick = () => {
      var learning = document.getElementById("learning").value;
      var discount = document.getElementById("discount").value;
      socket.emit('change', {'learn':learning, 'disc':discount});
    }
  })


  socket.on('new state', (board, message, qvalues) => {
    var butt = document.querySelectorAll('.thing');

    if (message != 'cont'){
      for (let i = 0; i < butt.length; i++) {
        butt[i].disabled = true;
      }
      document.getElementById('message').innerHTML = message;
    }

    document.getElementById('0').innerHTML = board[0][0];
    document.getElementById('1').innerHTML = board[0][1];
    document.getElementById('2').innerHTML = board[0][2];
    document.getElementById('3').innerHTML = board[1][0];
    document.getElementById('4').innerHTML = board[1][1];
    document.getElementById('5').innerHTML = board[1][2];
    document.getElementById('6').innerHTML = board[2][0];
    document.getElementById('7').innerHTML = board[2][1];
    document.getElementById('8').innerHTML = board[2][2];

    if (qvalues.length != 0){

      document.getElementById('00').innerHTML = qvalues[0];
      document.getElementById('01').innerHTML = qvalues[1];
      document.getElementById('02').innerHTML = qvalues[2];
      document.getElementById('03').innerHTML = qvalues[3];
      document.getElementById('04').innerHTML = qvalues[4];
      document.getElementById('05').innerHTML = qvalues[5];
      document.getElementById('06').innerHTML = qvalues[6];
      document.getElementById('07').innerHTML = qvalues[7];
      document.getElementById('08').innerHTML = qvalues[8];
    }
  })


  socket.on('invalid', () => {
    alert("Invalid Move");
  })
})
