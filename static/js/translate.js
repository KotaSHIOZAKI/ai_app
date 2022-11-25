function play_polly() {
    let ad = new Audio("static/audio/read_text.mp3");
    
    ad.play();
}

function swap_langage() {
    var lang1 = document.getElementById('lang1');
    var lang2 = document.getElementById('lang2');

    var saver = lang1.value;

    lang1.value = lang2.value;
    lang2.value = saver;
}