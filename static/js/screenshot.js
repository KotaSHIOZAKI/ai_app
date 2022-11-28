//引用：https://www.pahoo.org/e-soul/webtech/js01/js01-14-01.shtm

const FNAME_SAVE = 'sentiment';

function html2image(html) {
	var capture = document.querySelector(html);
	html2canvas(capture, {useCORS: true}).then(canvas => {
		var base64 = canvas.toDataURL();
        
		$('#download').attr('href', base64);
		$('#download').attr('download', FNAME_SAVE);
		$('#download')[0].click();				//自動ダウンロード
	});
}

$('#exec').on('click', function() {
    html2image('#screenshot', '#image');
});