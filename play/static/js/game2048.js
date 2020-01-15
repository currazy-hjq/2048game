var gamemap;
function drawmap(map) {
    var temp=[]
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            var item = '<div class="number_cell p' + i + j + '" ><div class="number_cell_con n'+map[i][j]+'"><span>'
                + map[i][j] + '</span></div> </div>';
            temp += item;
        }
    }
    $(".map").html(temp)
}
$('#gamebutton').click(function () {
    $.ajax({
        type: 'get',
        datatype: JSON,
        // url:baseurl+'/play',
        url: 'http://111.229.46.201:8000/game2048/init',
        success: function (response) {
            var temp = JSON.stringify(response)
            var data = JSON.parse(temp)
            gamemap = data.map
            drawmap(data.map)
        },
    })
})
$('#submitscore').click(function (){
    $('#namebox').addClass('namebox')
    var score = $('#score').text().substring(3)
    var html = '<div class="info" >当前分数:'+score+'</div>'
    html += '<div class="info">昵称<input type="text" id="username" placeholder="请输入你的游戏昵称"></div>'
    html += '<button id="submit">提交成绩</button>'
    $('#namebox').html(html)
    $('#submit').click(function (){
        var player = $('#username').val()
        $.ajax({
            type:'post',
            datatype:JSON,
            url:'http://111.229.46.201:8000/scorelist/add',
            data :JSON.stringify({'player':player,'score':score}),
            success:function(response){
                var temp = JSON.stringify(response)
                var data = JSON.parse(temp)
                if (data.code == 200){
                    $('#namebox').removeClass('namebox')
                    $('#namebox').html('')
                    alert('添加成功')
                }
            }
        })
        $('#gamebutton').click()
	$('#score').html("分数:0")
        //window.location.reload()
    })
})


document.addEventListener("keydown", keydown);
//键盘监听，注意：在非ie浏览器和非ie内核的浏览器
//参数1：表示事件，keydown:键盘向下按；参数2：表示要触发的事件
var dir='?';
function keydown(event) {
    //表示键盘监听所触发的事件，同时传递参数event
    switch (event.keyCode) {
        case 39://右
            dir = 'd';
            break;
        case 40://下
            dir = 's';
            break;
        case 37://左
            dir = 'a'
            break;
        case 38://上
            dir = 'w'
            break;
        default:
            dir = '?'
    }
    if (dir != '?'){
        $.ajax({
            type: 'post',
            datatype: JSON,
            // url:baseurl+'/play',
            url: 'http://111.229.46.201:8000/game2048/play',
            data :JSON.stringify({'dir':dir,'map':gamemap}) ,
            success: function (response) {
                var temp = JSON.stringify(response)
                var data = JSON.parse(temp)
                if (data.code == 200){
                    gamemap = data.map
                    drawmap(data.map)
                    var score = $('#score').text().substring(3)
                    score = parseInt(score) + parseInt(data.score)
                    $("#score").html("分数："+String(score));
                }else{
                    alert(data.error);
                }
            }
        })
    }
}

$('#scorelist').click(function () {
    window.open('http://111.229.46.201:8000/scorelist/init')
})

