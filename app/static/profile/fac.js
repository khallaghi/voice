$(document).ready(function(){
  $(".unis").select2({
    dir: "rtl",
    placeholder:"دانشکده را انتخاب کنید"

  });
  $(".faculties").select2({
    dir: "rtl",
    placeholder:"دانشکده را انتخاب کنید"
  });
  $(".faculties").hide();
  var $uniSelect = $(".unis");
      $.ajax(
      {
        type : "POST",
        url: "/faculty/search",
        data: JSON.stringify({
          uni: ($(".unis").select2("data"))[0]["id"]
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(result){
            console.log(result);
            $(".faculties").select2({
              data: null
            });
            $(".faculties").select2('data', {id: null, text: null});
            $(".faculties").select2({
              dir:"rtl",
              data: result.faculties,
              placeholder:"دانشکده را انتخاب کنید",
              allowClear: true
            });

      },
      error:function(){
        console.log("can't find anything ");
      }
    });

  $uniSelect.on("select2:open", function(e){
    // console.log("FUCK IT");
    $(".faculties").val('');
  });
  $uniSelect.on("select2:select", function(e){
    // var select2Data = [];
    console.log(e.params.data.id);

    $.ajax(
      {
        type : "POST",
        url: "/faculty/search",
        data: JSON.stringify({
          uni: e.params.data.id
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(result){
            console.log(result);
            $(".faculties").select2({
              data: null
            });
            $(".faculties").select2('data', {id: null, text: null});
            $(".faculties").select2({
              dir:"rtl",
              data: result.faculties,
              placeholder:"دانشکده را انتخاب کنید",
              allowClear: true
            });

      }
    });


    // ajax to server
  });
});
// jQuery(document).ready(function($){
//     // browser window scroll (in pixels) after which the "back to top" link is shown
//     var offset = 300,
//     //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
//         offset_opacity = 1200,
//     //duration of the top scrolling animation (in ms)
//         scroll_top_duration = 700,
//     //grab the "back to top" link
//         $back_to_top = $('.cd-top');

//     //hide or show the "back to top" link
//     $(window).scroll(function(){
//         ( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
//         if( $(this).scrollTop() > offset_opacity ) {
//             $back_to_top.addClass('cd-fade-out');
//         }
//     });

//     //smooth scroll to top
//     $back_to_top.on('click', function(event){
//         event.preventDefault();
//         $('body,html').animate({
//                 scrollTop: 0 ,
//             }, scroll_top_duration
//         );
//     });
// });