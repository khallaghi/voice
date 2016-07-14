$(document).ready(function(){
  $(".unis").select2({
    dir: "rtl"
  });
  // $(".faculties").select2();
  $(".faculties").hide();
  var $uniSelect = $(".unis");
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
