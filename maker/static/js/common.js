function lmt_log(log) {
    if(window.console && console.log) {
        console.log(log);
    }
}

/*====================botdocker pager begin ======*/
//For paginate directly full get request
function paginate_full_refresh(allPage, curPage,hrefUrl){
     pager_full_refresh(allPage, curPage);
     $(".pctype").click(function(ipage) {
         var ipage = $(this).attr('id');
         location.href = hrefUrl + '?page=' + ipage;
     });
}
//For ajax post
function pager_refresh(_json) {
    var allPage = parseInt(_json.allPage);
    var curPage = parseInt(_json.curPage);
    pager_full_refresh(allPage, curPage);
}
//For directly full get request
function pager_full_refresh(allPage, curPage) {
    lmt_log("curPage="+curPage+"allPage="+allPage);

    if (allPage <= 1) {
          //隐藏分页
           $("#page_nav").hide();
           return;
    } else {
           $("#page_nav").show();
    }

       //中间最多显示多少个页码
       var PAGE_NUM = 5;

        // 当前页面小于1,则为1
        if (curPage<1) {
            curPage = 1;
        }
        //当前页大于总页数,则为总页数
        if (curPage > allPage ) {
            curPage = allPage;
        }
        //页数小当前页 则为当前页
        if (allPage < curPage ) {
            allPage = curPage;
        }

        //计算开始页
        var start = curPage - Math.floor(PAGE_NUM/2);
        if (start < 1){
            start =1
        }

        //计算结束页
        var end = curPage + Math.floor(PAGE_NUM/2);
        if (end>allPage) {
            end =allPage;
        }

        lmt_log( 'start=' + start + '    end=' + end);

        //当前显示的页码个数不够最大页码数，进行左右调整
        var curPageNum = end-start+1;
        //左调整
        if (curPageNum<PAGE_NUM &&  start>1 ) {
            start = start - (PAGE_NUM-curPageNum);
            if (start < 1) {
                start =1;
                curPageNum = end-start+1;
            }
        }

        //右边调整
        if (curPageNum<PAGE_NUM && end<allPage ){
         end = end + (PAGE_NUM-curPageNum);
         if (end>allPage){
            end = allPage;
        }
    }

    var content = "";
    //上一页
    if (allPage>=1) {
        if (curPage>1 ){
            content += '<a class="pctype lastpage si si-zxgs-tag-lastpage_on" style="padding: 0px "  href="javascript:void(0);" id='+(curPage-1)+'></a>';
        } else {
            content += '<a class="lastpage si si-zxgs-tag-lastpage"></a>';
        }
    }

    //首页
    if (start > 1) {
        content += '<a class="pctype" href="javascript:void(0);" id="1" >1</a>';
    }

    //前面的...
    if  (start > 1) {
       content += '<i>...</i>';
   }

    //中间的
    for (i = start; i <= end; i++) {
        //首页 尾页 pass
          if (i == curPage ) {
              content += ' <a class="pctype pcchose" href="javascript:void(0);" id="'+i+'" >'+i+'</a>'
          }else {
              content += ' <a class="pctype" href="javascript:void(0);" id="'+i+'" >'+i+'</a>'
          }
  }

    //后面的...
    if (end < allPage ) {
       content+= '<i>...</i>'
   }

    //尾页
    if (allPage != 1 && allPage > end) {
            content += '<a class="pctype" href="javascript:void(0);" id="'+allPage+'" >'+allPage+'</a>';
    }

    //下一页
    if (allPage>=1) {
        if (curPage<end ) {
            content += '<a class="pctype nextpage si si-zxgs-tag-nextpage_on" style="padding: 0px " href="javascript:void(0);" id="'+(curPage+1)+'"></a>';
        } else {
            content += '<a class="nextpage si si-zxgs-tag-nextpage"></a>';
        }
    }

    $("#page_nav").html(content);
};
/*====================botdocker pager end ======*/

/*====================uc active begin ======*/
function cut_active(cur) {
    $('.treeview-menu li').removeClass('active');
    $('#' + cur).addClass('active');
    $('#' + cur).parent().show().prev().addClass('active');
    var lislen = $('.treeview-menu').length;
    for (var j = 0; j < lislen; j++) {
        if ($('.treeview-menu').eq(j).css('display') == 'block') {
            $('.treeview-menu').eq(j).find('a').addClass('text_name');
        } else {
            $('.treeview-menu').eq(j).find('a').removeClass('text_name');
        }
    }
    var text_name = $('.sidebar_nav .text_name');
    var lens = text_name.length;
    for (var q = 0; q < lens; q++) {
        text_name.eq(q).attr({
            y: (q + 1) * 40
        });
    }
};
/*====================uc active end ======*/