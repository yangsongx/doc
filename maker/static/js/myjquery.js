var sh=null;
var cartoon=null;
var words =null;// ret.split(':');
function query_result(){
    //alert("interval called"); 
    var myurl = "/wait/?"+"uuid="+words[1];
    //alert(myurl);
    //$.ajax(url:myurl, async:false, success:function(ret, textStatus, XMLHttpRequest){
    $.ajax({url:"/wait/", success:function(ret, textStatus, XMLHttpRequest){
    words =ret.split(':');
    if(words[0]!="wait_cal")
    {
        //alert("clear interval call");
        if(sh!=null)
            clearInterval(sh);
    }
    //alert(words[0]+"2ddd");
    $('#result').html(words[0])
 }
});
}
function show_cartoon(){
     var progress=""; 
     //for(var i='A';i<'Z';i++)
     {
         //progress=progress+"..";
         $('#result').html("cartoon");
     }

}
$(function(){
  $("#sum").click(function(){
    var a = $("#a").val();
    var b = $("#b").val();
    var myurl="/add/?"+"a="+a+"&"+"b="+b;
    //alert(myurl);
    /*
        pac_id: maker id

        pb_type_ID: resource type id ,for not prebuilt resourse, this is needed
        pb_info_ID: prebuilt info id
        name: uploaded file name
        download_url: download buket key on qiniu, for prebuilt resourse, set null
        suffix: unused
        modified: null
        crop: crop info for audio and imgs
        processed_url: processed url such as ringer
    */
    $.ajax({type:'POST', url:'/add/',async:true,dataType:'json',
             data:JSON.stringify({'makerID':"42a63333c6be031da7065b0ad3e6fdb5",
                                  data:[[4,126,null,null, null, null, null, null],
                                         [3,125,null,null, null, null, null, null],
                                         [5,-1,"com.imangi.templerun2",null, null, null, null, null],
                                         [1001, 10,null,null,null,null,null,null],
                                         [1002, 11,null,null,null,null,null,null],
                                         [1003, 12,null,null,null,null,null,null],
                                         [2, -1,"254531443cc2237fb18e26beb5e070d7_我的铃音.mp3","254531443cc2237fb18e26beb5e070d7",null,null,"86.875,100.625",null],
                                         [1, 9,null,null,null,null,null,null]],
/*
                                  data:[['boot-1', 'xxxx', 'xxx', null, '0'],
                                    ['boot-2', 'xxxx-2', 'xx', null, '1'],
                                    ['boot-3', 'xxxx-3', 'xx', 'xxxx', '0'],
                                    ['boot-4', null, null, null, null],
                                    ['uptone', 'xxxx-3.mp3', 'xx', 'xxxx', '0'],
                                    ['callringtone', 'xxxx-3.mp3', 'xxx', 'xxxx', '1'],
                                    ['lock', 'xxxx-3', 'xx', 'xxxx', '0'],
                                    ['welcome', 'hello world', null, null, null],
                                    ['app', 'com.halfbrick.fruitninja', '水果忍者', null, null],
                                    ['app', 'com.shootbubble.bubbledexlue', '泡泡龙', null, '1']],
*/
                   }),
             success:function(ret, textStatus, XMLHttpRequest){
                words = ret.split(':');
               if(words[0] == "task_running")
               {
                   alert("set up interval call");
                   sh=setInterval(query_result, 3000);
               }
               else
               {
                   ;//alert("not equal");
               }
               $('#result').html(a+"+"+b+"="+words[0])
             },
             beforeSend:function(){
               //alert("beforeSend");
               $('#result').append("<div><img src=\"/static/images/loading.gif\"/></div>");
             },
             complete:function(){
               //if(cartoon != null)
                //   clearInterval(cartoon);
               //alert("complete");
             },
             error:function(){
               alert("error");
             }
  });
 });
});

