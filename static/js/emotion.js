if (document.getElementById('emotionChart') != null) {
    var ctx = document.getElementById('emotionChart').getContext('2d');

    //円グラフで表すために、値を取得する。
    const positive = Math.round(Number(document.getElementById('positive').value) * 100);
    const negative = Math.round(Number(document.getElementById('negative').value) * 100);
    const neutral = Math.round(Number(document.getElementById('neutral').value) * 100);
    const mixed = Math.round(Number(document.getElementById('mixed').value) * 100);

    //円グラフの作成
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['😀肯定', '😡否定', '😐中立', '❓混合'],
            datasets: [{
                label: 'Emotion',
                backgroundColor: ["#1fe800", "#ff0000", "#ffdd00", "#00eeff"],
                borderColor: 'rgb(0, 0, 0)',
                data: [positive, negative, neutral, mixed]
            }]
        },
    });

    //一番多い割合の表情を可視化（中心に表示）
    var res = {
        "POSITIVE" : "😀",
        "NEGATIVE" : "😡",
        "NEUTRAL" : "😐",
        "MIXED" : "❓"
    };

    var chartJsPluginCenterLabel = {
        afterDatasetsDraw: function (chart) {
            // ラベルの X 座標と Y 座標
            var canvas = chart.ctx.canvas;
            var labelX = canvas.clientWidth / 2;
            var labelY = Math.round((canvas.clientHeight + chart.chartArea.top) / 2) + 6.25;
            // ラベルの値
            var value = res[document.getElementById('max').value];
            // ラベル描画
            var ctx = this.setTextStyle(chart.ctx);
            ctx.fillText(value, labelX, labelY);
        },
      
        /**
          * 書式設定
          */
        setTextStyle: function (ctx) {
            var fontSize = 100;
            var fontStyle = 'normal';
            var fontFamily = '"Helvetica Neue", Helvetica, Arial, sans-serif';
            ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);
            ctx.fillStyle = '#636363';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
        
            return ctx;
        }
    };

    Chart.plugins.register(chartJsPluginCenterLabel);
}

function changeText(input) {
    var text = document.getElementById('txt');

    //テキストファイルが読み込まれた時の処理
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        text.value = reader.result;
    };

    reader.readAsText(file);
}