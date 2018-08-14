/**
 * Created by Administrator on 2018/8/1.
 */

// CMS-用户管理-select:排序方式

$(function () {
   $('.sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = xtparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});