$('a.button').button();
$('button').button();

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//function getURLParameter(name) {
//    return decodeURI((new RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) || [, null])[1]);
//}
//
//
//$('.clickable[data-href]').on('click', function () { window.location = ($(this).attr('data-href'));})
//
//$('#viewprintprogramme').on('click', viewprintprogramme);
//
//if (location.search.indexOf('?vpp') >= 0) {
//    $('#viewprintprogramme').trigger('click');
//}
//
//function viewprintprogramme() {
//    var dialogdiv = $('<div id="dialogdiv">');
//    t = $(this);
//    t.append(dialogdiv);
//    $.ajax({
//        url:'/api/printprogramme/',
//        type:'POST',
//        dataType:'json',
//        data:{
//            'year':t.attr('data-year'),
//            'month':t.attr('data-month')
//        },
//        success:function (data) {
//            dialogdiv.empty();
//            for (var i = 0; i < data.sections.length; i++) {
//                dialogdiv.append($(data.sections[i]));
//            }
//            dialogdiv
//                .attr('title', data['title'])
//                .dialog({
//                    width:590,
//                    create:function (event, ui) {
//                        $("html").css('overflow', 'hidden');
//                    },
//                    beforeClose:function (event, ui) {
//                        $("html").css('overflow', 'inherit');
//                    }
//                });
//        }
//    });
//}
//

$('.picture').on('click.popupable', function () {
    var t = $(this);
    var dialogdiv = $('<div id="dialogdiv"></div>');
    var bigimg = $('<img alt="">')
        .attr('src', t.attr('data-src'))
        .attr('height', t.attr('data-height'))
        .attr('width', t.attr('data-width'));
    dialogdiv.append(bigimg);
    t.after(dialogdiv);
    dialogdiv
        .dialog({
            width: Math.min(parseInt(t.attr('data-width')) + 40, 1100),
            height: Math.min(parseInt(t.attr('data-height')) + 80, 800),
            close: function (event, ui) {
                $('#dialogdiv').remove();
            }
        });
});
