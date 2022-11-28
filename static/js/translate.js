function play_polly(path) {
    var ad = new Audio(path);
    
    ad.play();
}

function swap_langage() {
    var lang1 = document.getElementById('lang1');
    var lang2 = document.getElementById('lang2');

    var saver = lang1.value;

    lang1.value = lang2.value;
    lang2.value = saver;


    var txt1 = document.getElementById('sourceTxt');
    var txt2 = document.getElementById('resultText');

    saver = txt1.value;

    txt1.value = txt2.value;
    txt2.value = saver;
}