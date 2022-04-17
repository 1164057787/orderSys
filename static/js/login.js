$(function () {
    //登陆表单验证
    $('#btn').click(function () {
        var1=$('#inputEmail').val();
        var2=$('#inputPassword').val();

        if (var1.length<=0  ||  var2.length<=0){
            alert('用户名和密码不能为空');
        }
        console.log($('#inputEmail').val());
    });

})