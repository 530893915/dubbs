/**
 * Created by Administrator on 2018/8/1.
 */

// 前台-注册-btn：点击刷新图形验证码
$(function () {
    var btn = $('#graph-captcha-btn');
    btn.css('cursor','pointer');
    btn.css('padding','0');
    btn.click(function (event) {
       event.preventDefault();
       var imgTag = $(this).children('img');
       var oldSrc = imgTag.attr('src');
       var href = xtparam.setParam(oldSrc,'xx',Math.random());
       imgTag.attr('src',href);
    });
});