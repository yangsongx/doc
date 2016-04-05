function checkBrowser(){
   var u = window.navigator.userAgent.toLocaleLowerCase(),
    msie = /(msie) ([\d.]+)/,
    chrome = /(chrome)\/([\d.]+)/,
    firefox = /(firefox)\/([\d.]+)/,
    safari = /(safari)\/([\d.]+)/,
    opera = /(opera)\/([\d.]+)/,
    ie11 = /(trident)\/([\d.]+)/,
    b = u.match(msie)||u.match(chrome)||u.match(firefox)||u.match(safari)||u.match(opera)||u.match(ie11);
    return {name: b[1], version: parseInt(b[2])};

};
(function(jq){
	jq.fn.ppt = function(settings) {
		var html = '<div class="cover"><div class="bg"></div><div class="ppt"><a class="del" href="javascript:void(0)"></a><a class="lrow"  href="javascript:void(0)"></a><div class="lrow none"></div><div class="content"><ul id="pptUl">';
		html += '</ul></div><div class="info"><span class="describe"></span><span class="num">1/1</span></div><a class="rrow"  href="javascript:void(0)"></a><div class="rrow none"></div></div></div>';
		jq("body").append(html);
		
		var defaults = {
			oCover:"cover",//cover pannel
			oPpt:"ppt",//pic pannel
			oDel:"del",//shutdown
			oLeft:"lrow",//left row
			oRight:"rrow",//right row
			oClass:"show",//onshow li class
			isFirst:false,//is first pic or not,defines left row display
			isLast:false,//is last pic or not,defines right row display
			curNum:0
		};
		settings = jq.extend({},defaults,settings);
		var curObj = this;
		var ppt = {};
		ppt.fn = {};
		ppt.oCover = jq("." + settings.oCover);
		ppt.oPpt = jq("." + settings.oPpt);
		ppt.oDel = jq("." + settings.oDel);
		ppt.oLeft = jq("a." + settings.oLeft);
		ppt.oRight = jq("a." + settings.oRight);
		ppt.num = ppt.oPpt.find(".num");

		ppt.describe = ppt.oPpt.find(".describe");
		ppt.li = ppt.oCover.find("li");
		ppt.liNum = ppt.li.length;
		ppt.imgParent = jq(settings.imgParent);
		ppt.imgLi = ppt.imgParent.find("img");
		ppt.imgLiNum = ppt.imgLi.length;
		ppt.curNum = settings.curNum;
		
		ppt.fn.creatLi = function(e) {	
			var li = "";
			for(var i = 0;i < ppt.imgLiNum;i++) {
				if(ppt.curNum == i) {
					li += '<li class="show"  picname="'+jq(ppt.imgLi[i]).parents("li").find("span").text()+'"><img src='+jq(ppt.imgLi[i]).attr("data")+'></li>';	
				} else {
					li += '<li class="none"  picname="'+jq(ppt.imgLi[i]).parents("li").find("span").text()+'"><img src='+jq(ppt.imgLi[i]).attr("data")+'></li>';
				}
			}
			ppt.oPpt.find("#pptUl").append(li);	
			ppt.liNum = ppt.imgLiNum;
			ppt.num.html(ppt.curNum + 1 + "/" +ppt.liNum);		
		};
		
		/*ppt.fn.controlSize = function() {
			var ch = document.documentElement.clientHeight,
				cw = document.documentElement.clientWidth,
				h = (ch - 80),
				w = cw - 240;
			if(h >= 440) {
				ppt.oPpt.find(".content").css("top",(ch - 440)/2 + "px");
				ppt.oPpt.find(".info").css("top",(ch - 440)/2 + 441 + "px");	
			} else {
				ppt.oPpt.find(".content").css({"top":"40px","height":h+"px"});	
				ppt.oPpt.find(".info").css({"top":(h + 40) + "px"});	
				ppt.oPpt.find(".content>#pptUl>ul>li>img").css({"height":h+"px"});
			}
			ppt.oPpt.find(".lrow").css("top",(ch - 70)/2 + "px");
			ppt.oPpt.find(".rrow").css("top",(ch - 70)/2 + "px");
			if(w > 760) {
				ppt.oPpt.find(".content,.info").css({"left":(cw - 760)/2 + "px","margin-left":0});	
			} else {
				ppt.oPpt.find(".content,.info").css({"left":"120px","right":"120px","width":w+"px","margin-left":0});	
				ppt.oPpt.find(".content>#pptUl>ul>li>img,.info").css({"width":w+"px"});
			}	
		};*/
		ppt.fn.controlSize = function() {
			var ch = document.documentElement.clientHeight,
				cw = document.documentElement.clientWidth,
				h = (ch - 80),
				w = cw - 240;
			if(h >= 440) {
				ppt.oPpt.find(".content").css({"top":(ch - 440)/2 + "px","height":"440px"});
				ppt.oPpt.find(".info").css("top",(ch - 440)/2 + 441 + "px");	
			} else {
				ppt.oPpt.find(".content").css({"top":"40px","height":h+"px"});	
				ppt.oPpt.find(".info").css({"top":(h + 40) + "px"});	
				ppt.oPpt.find(".content>#pptUl>ul>li>img").css({"height":h+"px"});
			}
			ppt.oPpt.find(".lrow").css("top",(ch - 70)/2 + "px");
			ppt.oPpt.find(".rrow").css("top",(ch - 70)/2 + "px");
			if(w > 760) {
				ppt.oPpt.find(".content,.info").css({"left":(cw - 760)/2 + "px","margin-left":0,"width":"760px"});	
			} else {
				ppt.oPpt.find(".content,.info").css({"left":"120px","right":"120px","width":w+"px","margin-left":0});	
				ppt.oPpt.find(".content>#pptUl>ul>li>img,.info").css({"width":w+"px"});
			}	
		};
		
		ppt.fn.chkIe6css = function() {
			var obj = checkBrowser();
			if(obj.name == "msie" && obj.version == "6") {
				var h = jq(window).scrollTop();
				
				ppt.oPpt.css("top",h + "px");
				
				jq("html").css("overflow","hidden");
				jq("body").css({"height":"100%"});
			}
		};
		ppt.fn.moveIe6css = function() {
			var obj = checkBrowser();
			if(obj.name == "msie" && obj.version == "6") {
				jq("html").css("overflow","auto");
				//jq("body").css({"height":"auto"});
			}
		};
		//add Event Function
		ppt.fn.addControl = function() {
			ppt.li = ppt.oCover.find("li");
			ppt.liNum = ppt.li.length;
			ppt.fn.chkIe6css();
			ppt.oCover.show();
			ppt.oDel.bind("click",function() {
				ppt.fn.hideUl();	
				return false;
			});
			ppt.oLeft.bind("click",function() {
				ppt.fn.changeImg("dLeft");	
				return false;
			});
			ppt.oRight.bind("click",function() {
				ppt.fn.changeImg("dRight");	
				return false;
			});
			jq("div.lrow").bind("click",function() {
				return false;
			});
			jq("div.rrow").bind("click",function() {
				return false;
			});
			ppt.oCover.bind("click",function() {
				ppt.fn.hideUl();
			});
			
		};
		
		ppt.fn.hideUl = function() {	
			ppt.fn.moveIe6css();
			ppt.oCover.remove();
		};
		
		ppt.fn.changeImg = function(drec) {
			ppt.curNum = ppt.li.index(ppt.oCover.find("li[class="+settings.oClass+"]"));
			if(-1 == ppt.curNum) {
				ppt.curNum = 0;	
			}
			switch(drec) {
				case "dLeft":
				ppt.li.eq(ppt.curNum).removeClass(settings.oClass).addClass("none");
				ppt.li.eq(ppt.curNum - 1).removeClass("none").addClass(settings.oClass);
				ppt.num.html(ppt.curNum + "/" + ppt.liNum);
				ppt.describe.html(ppt.li.eq(ppt.curNum - 1).attr("picname"));
				ppt.fn.showRrow();
				
				if(1 == ppt.curNum) {//first hide left
					ppt.fn.hideLrow();
				}	
				break;
				case "dRight":
				ppt.li.eq(ppt.curNum).removeClass(settings.oClass).addClass("none");
				ppt.li.eq(ppt.curNum + 1).removeClass("none").addClass(settings.oClass);
				ppt.num.html(ppt.curNum + 2 + "/" + ppt.liNum);
				ppt.describe.html(ppt.li.eq(ppt.curNum + 1).attr("picname"));
				ppt.fn.showLrow();
				
				if(ppt.liNum == ppt.curNum + 2) {//last hide right
					ppt.fn.hideRrow();
				}
				break;
			}	
		};
		
		ppt.fn.hideLrow = function() {
			ppt.oLeft.hide();
			jq("div.lrow").show();	
		};
		
		ppt.fn.hideRrow = function() {
			ppt.oRight.hide();	
			jq("div.rrow").show();	
		};
		
		ppt.fn.showLrow = function() {
			ppt.oLeft.show();
			jq("div.lrow").hide();	
		};
		
		ppt.fn.showRrow = function() {
			ppt.oRight.show();	
			jq("div.rrow").hide();	
		};
		
		ppt.fn.init = function() {
			ppt.fn.creatLi();
			ppt.fn.addControl();
			var height =(jq("body").height() > jq("html").height())?jq("body").height():jq("html").height();
			ppt.oCover.height(height); 
			
			if(1 == ppt.liNum) {
				settings.isFirst = true;	
				settings.isLast = true;
			}
			if(0 != ppt.curNum) {
				settings.isFirst = false;	
			} else {
				settings.isFirst = true;		
			}
			if(ppt.liNum != ppt.curNum + 1) {
				settings.isLast = false;	
			} else {
				settings.isLast = true;	
			}
			if(settings.isFirst) {
				ppt.fn.hideLrow();	
			}
			if(settings.isLast) {
				ppt.fn.hideRrow();
			}
			ppt.curNum = ppt.li.index(ppt.oCover.find("li[class="+settings.oClass+"]"));
			ppt.describe.html(ppt.li.eq(ppt.curNum).attr("picname"));
			ppt.fn.controlSize();
			jq(window).bind("resize",function() {
				ppt.fn.controlSize();	
			});
		}
		ppt.fn.init();
	};
})(jQuery);