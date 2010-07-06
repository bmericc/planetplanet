var BrowserDetect = {
	init: function(){
		this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
		this.version = this.searchVersion(navigator.userAgent) ||
		this.searchVersion(navigator.appVersion) ||
		"an unknown version";
	},
	searchString: function(data){
		for (var i = 0; i < data.length; i++) {
			var dataString = data[i].string;
			var dataProp = data[i].prop;
			this.versionSearchString = data[i].versionSearch || data[i].identity;
			if (dataString) {
				if (dataString.indexOf(data[i].subString) != -1) 
					return data[i].identity;
			}
			else 
				if (dataProp) 
					return data[i].identity;
		}
	},
	searchVersion: function(dataString){
		var index = dataString.indexOf(this.versionSearchString);
		if (index == -1) 
			return;
		return parseFloat(dataString.substring(index + this.versionSearchString.length + 1));
	},
	dataBrowser: [{
		string: navigator.userAgent,
		subString: "Chrome",
		identity: "Chrome"
	},
	{
		string: navigator.vendor,
		subString: "Apple",
		identity: "Safari"
	}, {
		prop: window.opera,
		identity: "Opera"
	}, {
		string: navigator.userAgent,
		subString: "Flock",
		identity: "Flock"
	}, {
		string: navigator.userAgent,
		subString: "Firefox",
		identity: "Firefox"
	}, {
		string: navigator.userAgent,
		subString: "MSIE",
		identity: "IExplorer",
		versionSearch: "MSIE"
	}]
};
var BrowserCompatible = {
	check: function(){
		BrowserDetect.init();
		if ((this.useBlackList && this.unCompatibleBrowsers[BrowserDetect.browser] && BrowserDetect.version <= this.unCompatibleBrowsers[BrowserDetect.browser]) ||
		    (!this.useBlackList && (BrowserDetect.version < this.compatibleBrowsers[BrowserDetect.browser] || !this.compatibleBrowsers[BrowserDetect.browser]))) {
			if (!this.readCookie('browsercheck_dontShowAgain')) 
				this.showWarning();
		}
	},
	getStyle: function(el, styleProp){
		var x = el;
		if (x.currentStyle) 
			var y = x.currentStyle[styleProp];
		else 
			if (window.getComputedStyle) 
				var y = document.defaultView.getComputedStyle(x, null).getPropertyValue(styleProp);
		return y;
	},
	createCookie: function(name, value, days){
		if (days) {
			var date = new Date();
			date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
			var expires = ";expires=" + date.toGMTString();
		}
		else 
			var expires = "";
		document.cookie = name + "=" + value + expires + ";path=/";
	},
	
	readCookie: function(name){
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for (var i = 0; i < ca.length; i++) {
			var c = ca[i];
			while (c.charAt(0) == ' ') 
				c = c.substring(1, c.length);
			if (c.indexOf(nameEQ) == 0) 
				return c.substring(nameEQ.length, c.length);
		}
		return null;
	},
	
	eraseCookie: function(name){
		this.createCookie(name, "", -1);
	},
	showWarning: function(){
		if(!this.lang){
			this.lang=navigator.language || navigator.browserLanguage;
			if(!this.langTranslations[this.lang]) this.lang="en";
		}
		var bg = document.createElement("div");
		bg.id = "browsercheck_bg";
		bg.style["background"] = "#fff";
		bg.style["filter"] = "alpha(opacity=90)";
		bg.style["-moz-opacity"] = "0.90";
		bg.style["opacity"] = "0.9";
		bg.style["position"] = "fixed";
		if (BrowserDetect.browser == "IExplorer" && BrowserDetect.version < 7) 
			bg.style["position"] = "absolute";
		bg.style["z-index"] = "9998";
		bg.style["top"] = "0";
		bg.style["left"] = "0";
		bg.style["height"] = (screen.availHeight + 300) + "px";
		bg.style["width"] = (screen.availWidth + 300) + "px";
		
		var warning_html = "";
		if (this.allowCancel) 
			warning_html += '<a href="javascript:BrowserCompatible.cancel()" style="background:url('+this.images['cancel']+') no-repeat; height:15px; width:16px; position:absolute; right:10px; top:7px;" title="' + this.langTranslations[this.lang]['cancel'] + '"></a>';
		warning_html += '<div id="browsercheck_title" style="font-family:arial; font-size:24px; color:#000; margin:15px;">' + this.langTranslations[this.lang]['title'] + '</div>';
		warning_html += '<div id="browsercheck_description" style="font-family:arial; font-size:12px; color:#707070;	 margin:15px;">' + this.langTranslations[this.lang]['description'] + '</div>';
		warning_html += '<div id="browsercheck_recomendation" style="font-family:arial; font-size:12px; color:#707070; margin:15px;">' + this.langTranslations[this.lang]['recomendation'] + '</div>';
		for (var i = 0; i < this.offeredBrowsers.length; i++) {
			warning_html += '<a href="' + this.browsersList[this.offeredBrowsers[i]].link + '" title="' + this.langTranslations[this.lang][this.offeredBrowsers[i]] + '" style="height:60px; width:165px; display:block; float:left; margin:15px; text-decoration:none; background: url(' + this.browsersList[this.offeredBrowsers[i]].image + ') no-repeat;" target="_blank"> </a>';
			
		}
		if (this.allowToHide) 
			warning_html += '<div style="clear:both;font-family:arial; font-size:12px; color:#707070; padding:7px 15px;"><label><input type="checkbox" id="browsercheck_dontShowAgain" onclick="BrowserCompatible.dontShowAgain()" />' + this.langTranslations[this.lang]['dontShowAgain'] + '</label></div>';
		var warning = document.createElement("div");
		warning.id = "browsercheck_warning";
		warning.style["background"] = "url("+this.images['background']+") no-repeat";
		warning.style["padding"] = "2px";
		warning.style["width"] = "600px";
		warning.style["height"] = "400px";
		warning.style["position"] = "fixed";
		if (BrowserDetect.browser == "IExplorer" && BrowserDetect.version < 7) 
			warning.style["position"] = "absolute";
		warning.style["z-index"] = "9999";
		warning.style["top"] = ((window.innerHeight || document.body.parentNode.offsetHeight) - 400) / 2 + "px";
		warning.style["left"] = ((window.innerWidth || document.body.parentNode.offsetWidth) - 600) / 2 + "px";
		warning.innerHTML = warning_html;
		
		this.old_overflow_style = this.getStyle(document.body.parentNode, "overflow") || this.getStyle(document.body, "overflow");
		if (BrowserDetect.browser == "Opera" && this.old_overflow_style == "visible") 
			this.old_overflow_style = "auto";
		document.body.parentNode.style["overflow"] = "hidden";
		document.body.style["overflow"] = "hidden";
		
		document.body.appendChild(bg);
		document.body.appendChild(warning);
		
		if (document.addEventListener) {
			document.addEventListener('resize', this.warningPosition, false);
		}
		else {
			document.attachEvent('onresize', this.warningPosition);
		}
		
	},
	warningPosition: function(){
		var warning = document.getElementById('browsercheck_warning');
		warning.style["top"] = ((window.innerHeight || document.body.parentNode.offsetHeight) - 400) / 2 + "px";
		warning.style["left"] = ((window.innerWidth || document.body.parentNode.offsetWidth) - 600) / 2 + "px";
	},
	dontShowAgain: function(){
		var inpDontShowAgain = document.getElementById('browsercheck_dontShowAgain').checked;
		var dontShowAgain = this.readCookie('browsercheck_dontShowAgain');
		if (inpDontShowAgain) {
			this.createCookie('browsercheck_dontShowAgain', 'on', this.cookiesExpire);
		}
		else {
			this.eraseCookie('browsercheck_dontShowAgain');
		}
	},
	cancel: function(){
		var bg = document.getElementById('browsercheck_bg');
		var warning = document.getElementById('browsercheck_warning');
		bg.parentNode.removeChild(bg);
		warning.parentNode.removeChild(warning);
		document.body.parentNode.style["overflow"] = this.old_overflow_style;
		if (BrowserDetect.browser != "IExplorer") 
			document.body.style["overflow"] = this.old_overflow_style;
		document.onresize = this.resize_function;
	},
	old_overflow_style: "",
	resize_function: null,
	allowCancel: false,
	allowToHide: false,
	cookiesExpire: 1,
	images : {
		'background':"img/bg.gif",
		'cancel':"img/cancel.gif"
	},
	useBlackList: false,
	compatibleBrowsers: {
		"Opera": 9.25,
		"Firefox": 2,
		"IExplorer": 7,
		"Safari": 525.17,
		"Flock": 1.1,
		"Chrome": 1
	},		
	unCompatibleBrowsers: {
		"IExplorer": 6
	},
	offeredBrowsers: ["Chrome","Firefox", "Flock", "Safari", "IExplorer", "Opera"],
	browsersList: {
		"Chrome": {
			"image": "http://www.goodbyeie6.org.ua/chrome.gif",
			"link": "http://www.google.com/chrome/"
		},
		"Opera": {
			"image": "http://www.goodbyeie6.org.ua/opera.gif",
			"link": "http://www.opera.com/products/desktop/"
		},
		"Firefox": {
			"image": "http://www.goodbyeie6.org.ua/firefox.gif",
			"link": "http://www.mozilla-europe.org/"
		},
		"IExplorer": {
			"image": "http://www.goodbyeie6.org.ua/iexplorer.gif",
			"link": "http://www.microsoft.com/windows/internet-explorer/download-ie.aspx"
		},
		"Safari": {
			"image": "http://www.goodbyeie6.org.ua/safari.gif",
			"link": "http://www.apple.com/safari/"
		},
		"Flock": {
			"image": "http://www.goodbyeie6.org.ua/flock.gif",
			"link": "http://www.flock.com/"
		}
	},
	lang: "",
	langTranslations: {
		"uk": {
			"title": "Несумісний браузер",
			"description": "Ваш браузер вже застарів, тому в ньому немає всіх необхідних функцій для коректної роботи веб-сайтів. Сучасні веб-сайти створюються, щоб бути максимально зручними та максимально ефективними для людини, а разом із удосконаленням сайтів покращуються браузери. Крім цього, з розвитком інтернет-комерції, зростає кількість зловмисників та хакерських атак; використання найновіших версій браузерів - хороший спосіб вберегти свій комп'ютер.",
			"recomendation": "Ми рекомендуємо використовувати останню версію одного із наступних браузерів:",
			"cancel": "Закрити попередження",
			"dontShowAgain": "Не показувати це попередження наступного разу",
			"Flock": "Браузер Flock спеціалізований для користувачів різноманітних соціальних мереж. \nВін оснований на тому ж двигуні що й Firefox, тому демонструє таку ж стабільність та корекність роботи.",
			"Firefox": "На сьогоднішній день найпопулярніший браузер у світі. \nЗагальне число користувачів браузера Firefox становить 40%.",
			"IExplorer": "Браузер Internet Explorer від компанії Microsoft з 7-ї версії вийшов на новий рівень. \nПроте все ж поступається за коректністю роботи іншим браузерам.",
			"Safari": "Популярний браузер від компанії Apple. \nЗ версії 3.1 демонструє достатню стабільність, за що й потрапив до цього списку.",
			"Opera": "Браузер Opera користується популярністю в Європі, але великі компанії досі його ігнорують. \nOpera має низку недоліків, проте стабільно удосконалюється.",
			"Chrome": "Браузер Chrome - молодий браузер створений компанією Google. \nРозробники приділили особливу увагу зручності браузера, і разом з тим він ні скільки не поступається за коректністю роботи."
		},
		"ru": {
			"title": "Несовместимый браузер",
			"description": "Ваш браузер уже устарел, потому в нем нет всех необходимых функций для корректной работы веб-сайтов. Современные веб-сайты создаются, чтобы быть максимально удобными и максимально эффективными для человека, а вместе с усовершенствованием сайтов улучшаются браузеры. Кроме этого, с развитием интернет-комерции, растет количество злоумышленников и хакерских атак; использование новейших версий браузеров - хороший способ уберечь свой компьютер.",
			"recomendation": "Мы рекомендуем использовать последнюю версию одного из следующих браузеров:",
			"cancel": "Закрыть предупреждение",
			"dontShowAgain": "Не показывать это предупреждение вновь",
			"Flock": "Браузер Flock специализирован для пользователей разнообразных социальных сетей. \nОн основан на том же движке что и Firefox, потому демонстрирует такую же стабильность и коректность работы.",
			"Firefox": "На сегодняшний день самый популярный браузер в мире. \nОбщее число пользователей браузера Firefox составляет 40%.",
			"IExplorer": "Браузер Internet Explorer от компании Microsoft после 7-и версии вышел на новый уровень. \nОднако все же уступает за корректностью работы другим браузерам.",
			"Safari": "Популярный браузер от компании Apple. \nПосле версии 3.1 демонстрирует достаточную стабильность, за что и попал к этому списку.",
			"Opera": "Браузер Opera пользуется популярностью в Европе, но большие компании до сих пор его игнорируют. \nOpera имеет ряд недостатков, однако стабильно совершенствуется.",
			"Chrome": "Браузер Chrome - молодой браузер созданный компанией Google. \nРазработчики уделили особое внимание удобству браузера, и вместе с тем он ни сколько не уступает по коректнистю работы."
		},
		"en": {
			"title": "Desteklenmeyen Tarayıcı!",
			"description": "Tarayıcınız web sayfamız tarafından artık desteklenmiyor. Bu da demek oluyor ki sayfamızı verimli olarak kullanamayacaksınız. Lütfen aşağıdaki tarayıcılardan birini kurun.",
			"recomendation": "",
			"cancel": "Bu uyarıyı kapat",
			"dontShowAgain": "Bu uyarıyı tekrar gösterme",
			"Firefox": "",
			"Flock": "",
			"IExplorer": "",
			"Safari": "",
			"Opera": "",
			"Chrome" : ""
		}
	}
}