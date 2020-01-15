var index
function loadlist(pageindex){
    index=pageindex
    $.ajax({
        type: 'get',
        // dataType: JSON,
        url: 'http://111.229.46.201:8000/scorelist/show?page='+String(pageindex),
        success: function(response){
            var temp = JSON.stringify(response)
            var data = JSON.parse(temp)
            if (data.code == 200){
                var html = '<tr><th>排名</th><th>昵称</th><th>分数</th></tr>'
                var number = (pageindex-1)*5+1
                console.log(number)
                for (var item of data.listinfo){
                    html += '<tr><td>'+String(number)+'</td><td>'+item.player+'</td><td>'+item['score']+'</td></tr>'
                    number += 1
                }
                $('table').html(html)
            }else{
                alert(data.error)
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
                // 状态码
                console.log(XMLHttpRequest.status);
                // 状态
                console.log(XMLHttpRequest.readyState);
                // 错误信息   
                console.log(textStatus);
            }
            
    })
}
loadlist(1)
$('#lastpage').click(function(){
        loadlist(index-1)
    })
$('#nextpage').click(function(){
        loadlist(index+1)
    })
