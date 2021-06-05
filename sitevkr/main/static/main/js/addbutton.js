
let inputs = document.querySelectorAll('.input__file');
Array.prototype.forEach.call(inputs, function (input) {
    let label = input.nextElementSibling,
    labelVal = label.querySelector('.input__file-button-text').innerText;
    input.addEventListener('change', function (e) {
        let countFiles = '';
        if (this.files && this.files.length >= 1)
          countFiles = this.files.length;

        if (countFiles)
          label.querySelector('.input__file-button-text').innerText = 'Выбран файл: ' + this.files[0].name;
        else
          label.querySelector('.input__file-button-text').innerText = labelVal;
      });
    });
