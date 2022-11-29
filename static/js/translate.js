// function play_polly(path) {
//     var ad = new Audio(path);
    
//     ad.play();
// }

window.onload = function () {
    var saver1 = document.getElementById('lang1saver');
    var saver2 = document.getElementById('lang2saver');

    if (saver1.value == "" || saver2.value == "") {
        //送信されていない場合
        return;
    }

    //送信されたときに、各言語を保持
    var lang1 = document.getElementById('lang1');
    var lang2 = document.getElementById('lang2');

    lang1.value = saver1.value;
    lang2.value = saver2.value;
}

function swap_langage() {
    //取得
    var lang1 = document.getElementById('lang1');
    var lang2 = document.getElementById('lang2');
    //数値を保管する変数
    var saver = lang1.value;
    //入れ替える
    lang1.value = lang2.value;
    lang2.value = saver;

    //テキスト
    var txt1 = document.getElementById('sourceTxt');
    var txt2 = document.getElementById('resultText');
    //数値を保管
    saver = txt1.value;
    //入れ替える
    txt1.value = txt2.value;
    txt2.value = saver;
}