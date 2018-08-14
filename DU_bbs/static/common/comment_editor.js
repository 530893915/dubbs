/**
 * Created by Administrator on 2018/8/7.
 */

/// 初始化七牛的事件
$(function () {
    var progressBox = $('#progress-box');
    var progressBar = progressBox.children(0);
    var uploadBtn = $('#upload-btn');
    xtqiniu.setUp({
         'browse_btn': 'upload-btn',
         'success': function (up,file,info) {
             var fileUrl = file.name;
             if(file.type.indexOf('video') >= 0){
                // 视频
                 var videoTag = "<video width='640' height='480' controls><source src="+fileUrl+"></video>";
                 window.editor.txt.append(videoTag);
             }else{
                 // 图片
                 var imgTag = "<img src="+fileUrl+">";
                 window.editor.txt.append(imgTag);
             }
         },
         'fileadded':function () {
             progressBox.show();
             uploadBtn.button('loading');
          },
         'progress':function (up, file) {
             var percent = file.percent;
             progressBar.attr('aria-valuenow',percent);
           progressBar.css('width',percent+'%');
           progressBar.text(percent+'%');
         },
         'complete':function(){
             progressBox.hide();
             progressBar.attr('aria-valuenow',0);
             progressBar.css('width','0%');
             progressBar.text('0%');
             uploadBtn.button('reset');
         }
   });
});
