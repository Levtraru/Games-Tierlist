var input = document.getElementById('txtImagen');
  var label = input.nextElementSibling,
    labelVal  = label.innerHTML;
  
  input.addEventListener('change', (e) => {
    var fileName = '';
    fileName = e.target.value.split('\\').pop();
    if (fileName) {
      label.innerHTML = fileName;
      label.style.backgroundColor = 'var(--white)';
      label.style.color = 'var(--black)';
    } else {
      label.innerHTML = labelVal;
    }
  });