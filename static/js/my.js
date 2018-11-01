/**
 * Created by dongyibo on 2018/4/29.
 */
//舍弃簇
function abort(id, category, appId, span) {
    if (!confirm("Do you want to abort it?")) {
        return;
    }
    // alert(id)
    //开始异步传输数据
    $.ajax({
        type: 'GET',
        url: '/abortAjax?category=' + category + '&appId=' + appId + '&id=' + id,
        dataType: 'json',
        success: $(span).parent().parent().parent().hide(),
        error: function (xhr, type) {
            alert(xhr.status);
            alert(xhr.readyState);
            alert(type);
        }
    });
}

//恢复簇
function recover(id, category, appId, span) {
    if (!confirm("Do you want to recover it?")) {
        return;
    }
    //开始异步传输数据
    $.ajax({
        type: 'GET',
        url: '/recoverAjax?category=' + category + '&appId=' + appId + '&id=' + id,
        dataType: 'json',
        success: $(span).parent().parent().parent().hide(),
        error: function (xhr, type) {
            alert(xhr.status);
            alert(xhr.readyState);
            alert(type);
        }
    });
}

//更过内容
function more(btn) {
    par = $(btn).parent().parent();
    par.hide();
    par.siblings("li").show();
    par.siblings("div").show();
}

//卷起
function roll(btn) {
    par = $(btn).parent().parent();
    par.siblings(".roll-up").hide();
    par.hide();
    par.siblings("div").show();
}

