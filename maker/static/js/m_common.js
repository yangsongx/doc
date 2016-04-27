/*====================mobile botdocker pager begin ======*/
//For paginate directly full get request
function m_paginate_full_refresh(allPage, curPage,hrefUrl){
    jq(".widget-pagination-pages").change(function(event) {
       var ipage =  jq(this).find("option:selected").val();
         location.href = hrefUrl + '?page=' + ipage;
    });

    jq(".pctype").click(function(ipage) {
         var ipage = jq(this).attr('id');
         location.href = hrefUrl + '?page=' + ipage;
     });
}

function m_pager_refresh(_json) {
    var allPage = parseInt(_json.allPage);
    var curPage = parseInt(_json.curPage);
    m_log("curPage="+curPage+"allPage="+allPage);

    if (allPage <= 1) {
          //隐藏分页
           jq("#page_nav").hide();
           return;
    } else {
           jq("#page_nav").show();
    }

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

    var content = "";
    //上一页
    if (allPage>=1) {
        if (curPage>1 ){
            content += '<a class="pctype" href="javascript:void(0);" id='+(curPage-1)+'>上一页</a>';
        } else {
            content += '<a class="widget-pagination-disable" href="javascript:;">上一页</a>';
        }
    }

    //中间的
    content += '<div>';
    content += '<a class="widget-pagination-current-page">'+curPage+'/'+allPage+'</a>';
    content += '<select class="widget-pagination-pages needsclick" id="pageCounts">';
     for (i = 1; i <= allPage; i++) {
          if (i == curPage ) {
              content += '<option selected=\‘selected\’ value="'+i+'" >'+i+'/'+allPage+'</option>'
          }else {
          	 content += '<option value="'+i+'" >'+i+'/'+allPage+'</option>'
          }
     }
     content += '</select>';
     content += '</div>';

    //下一页
    if (allPage>=1) {
        if (curPage<allPage ) {
            content += '<a class="pctype" href="javascript:void(0);" id='+(curPage+1)+'>下一页</a>';
        } else {
            content += '<a class="pctype widget-pagination-disable" href="javascript:;">下一页</a>';
        }
    }

    jq("#page_nav").html(content);
};
/*====================mobile botdocker pager end ======*/