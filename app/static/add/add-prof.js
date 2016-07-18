$(document).ready(function(){
  $("#uni").select2({
    dir: "rtl",
    placeholder:"دانشکده را انتخاب کنید"

  });
  $("#faculty").select2();
  // $(".faculties").hide();
  var $uniSelect = $("#uni");
  $uniSelect.on("select2:select", function(e){
    var select2Data = [];
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
            $("#faculty").select2({
              data: null
            });
            $("#faculty").select2('data', {id: null, text: null});
            $("#faculty").select2({
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
