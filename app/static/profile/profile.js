
var app = angular.module('profile', ['vcRecaptcha']);
app.controller('rating', function(){
    var el = document.querySelector('#el');

    var currentRating = 0;

    var maxRating= 5;

    var callback = function(rating) { alert(rating); };

    var myRating = rating(el, currentRating, maxRating, callback);
});
app.controller('Comment', function(reportComment, Scopes, $scope){
    var dict = {
        "coolness":{
            1:"نه اصلا",
            2:"نه. معمولیه",
            3:"ای یکمی",
            4:"آره باحاله",
            5:"خیلی زیاد"
        },
        "useTextbook":{
            1:"آره",
            2:"نه"
        },
        "attendance":{
            1:"آره همیشه",
            2:"بعضی وقتا",
            3:"نه اصلا"
        }
    }
    $scope.get_comments = function(){
        return Scopes.get('comments');
    };
    $scope.result_gen = function(key, id){
        return dict[key][id.toString()];
    };
    $scope.report_cmt = function(cmt_id){
        // prof_id = Scopes.get("prof_id");
        reportComment.async(cmt_id).then(function(d){
            if(d.success == true)
                alert("درخواست شما با موفقیت ثبت شد");
            else
                alert("ثبت درخواست شما با مشکل روبرو شد");
        });
    };
    $scope.calcPercent = function(val){
        var maximum = 5;
        return val/maximum*100;
    }
});


app.controller('mainResult', function(myService, Scopes, $scope){
    var results = undefined;
    $scope.study_count = 0;
    var save_json = function(res){
        this.result = res;
    };

	$scope.chart = function(result){
            Highcharts.chart('main-result', {
    	    chart: {
                type: 'column',
                // marginRight: 130,
                marginBottom: 25,
                renderTo: 'container',
                margin: 0,
                backgroundColor:'rgba(255, 255, 255, 0)'
            },
            title: {
                enabled: false,
                text: '',
            },
            xAxis: {
                categories: ['clarity', 'easiness', 'helpfulness'],
                labels: {
                    formatter: function(){
                        return '<div class = "container"><b>' + this.value + '</b></div>';
                    }
                },

                lineWidth: 0,
                minorGridLineWidth: 0,
                lineColor: 'transparent',
            },
            yAxis: {
                min: 0,
                max: 5,
                // gridLineWidth: 0,
                // minorGridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
            },
            plotOptions: {
                column: {
                    dataLabels: {
                        enabled: false
                    },
                shadow: false,
                center: ['50%', '50%'],
                borderWidth: 0 // < set this option
                },
            },
            legend:{
                enabled: false,
            },
            credits: {
                enabled: false
            },
            tooltip: {
                 formatter: function() {
                    return '<b>' + this.y + '</b>';
                  }
                // enabled: true
            },
            series: [{
                data: [ {

                        y: result.main_result.clarity.value,
                        // y: 7,
                        name: "clarity",
                        color: result.main_result.clarity.color
                    },{

                        y: result.main_result.easiness.value,
                        // y: 8,
                        name: "Easiness",
                        color: result.main_result.easiness.color
                    },{

                        y: result.main_result.helpfulness.value,
                        // y: 9,
                        name: "Helpfulness",
                        color: result.main_result.helpfulness.color
                    }
                    ]
            }]
        });
    };
    $scope.study_chart = function(result,i){
      Highcharts.chart('study-result-'+i.toString(), {
            chart: {
                // type: 'solidgauge',
                // polar: true,
                type: 'column',
                // marginRight: 130,
                marginBottom: 25,
                // renderTo: 'study-result',
                margin: 0,
                backgroundColor:'rgba(255, 255, 255, 0)'
            },
            title: {
                formatter: function(){
                    return '<b>' + this.value + '</b>'
                },
                enabled: false,
                text: result.name,
            },
            xAxis: {
                categories: ['clarity', 'easiness', 'helpfulness'],
                lineWidth: 0,
                minorGridLineWidth: 0,
                lineColor: 'transparent',
            },
             tooltip: {
                 formatter: function() {
                    return '<b>' + this.y + '</b>';
                  }
                // enabled: true
            },
            yAxis: {
                min: 0,
                max: 5,
                // gridLineWidth: 0,
                // minorGridLineWidth: 0,
                labels: {
                    enabled: false
                },
                title: {
                    text: null
                },
            },
            plotOptions: {
                column: {
                    dataLabels: {
                        enabled: false
                    },
                shadow: false,
                center: ['50%', '50%'],
                borderWidth: 0 // < set this option
                },
            },
            legend:{
                enabled: false,
            },
            credits: {
                enabled: false
            },

            legend:{
                enabled: false,
            },
            credits: {
                enabled: false
            },
            series: [{
                data: [{

                        y: result.clarity.value,
                        // y: 7,
                        name: "clarity",
                        color: result.clarity.color
                    },{

                        y: result.easiness.value,
                        // y: 8,
                        name: "Easiness",
                        color: result.easiness.color
                    },{

                        y: result.helpfulness.value,
                        // y: 9,
                        name: "Helpfulness",
                        color: result.helpfulness.color
                    }
                    ]
            }]
        });
    };


    $scope.init = function(id){
        this.id = id;
        Scopes.store("prof_id", id);
        myService.async(this.id).then(function(d) {
            $scope.data = d;
            $scope.chart($scope.data);
            $scope.study_count = $scope.data.studies_result.length;
            var comments = $scope.data.comments;
            Scopes.store("comments", comments);
            Scopes.store("personal_tags", $scope.data.personal_tags);
            Scopes.store('study_count', $scope.study_count);
            for(i = 0; i < $scope.data.studies_result.length; i++){
                $scope.study_chart($scope.data.studies_result[i],i);
            }
            getCourses($scope.data.studies_result);

        });
    };
});
app.controller('chart', function(Scopes, $scope){
    $scope.chart_count = function(){
        return Scopes.get('study_count');
    }
});

app.controller('TagCtrl', function(Scopes, $scope){
    $scope.get_personal_tags = function(){
        return Scopes.get('personal_tags');
    };
    $scope.convert_num = function(num){
        return num;
    }
});
app.controller('MainCtrl', ['$scope', '$http', '$controller', 'vcRecaptchaService' ,function($scope, $http, $controller, vcRecaptchaService) {
    $scope.resopnse = null;
    // $scope.gRecaptchaResponse = null;
    $scope.init = function(id){
        $scope.id = id;
    };
    $scope.submit = false;
    var validateScore = function(score){
        if(score <= 6 && score > 0)
            return true;
        return false;
    };
    $scope.helpfulness = 0;
    $scope.setHelpfulness = function(score){
        if(validateScore(score)){
            $scope.helpfulness = score;
        }
    };

    // $scope.comment = "";
    $scope.easiness = 0;
    $scope.setEasiness = function(score){
        if(validateScore(score)){
            $scope.easiness = score;
        }
    };
    $scope.clarity = 0;
    $scope.setClarity = function(score){
        if(validateScore(score)){
            $scope.clarity = score;
        }
    };

    $scope.coolness = 0;
    $scope.setCoolness = function(score){
        if(validateScore(score))
            $scope.coolness = score;
    };

    $scope.useTextbook = 0;
    $scope.setUseTextbook = function(score){
        if(score<=2 && score>=0)
            $scope.useTextbook = score;
    };

    $scope.attendance = 0;
    $scope.setAttendance = function(score){

        if(score<=3 && score>0){
            $scope.attendance = score;
        }
    };
    $scope.selectedTagsCount = 0;
    $scope.allTags = [{
                            name:'انگیزه‌دهنده',
                            status: 0
                        },
                        {
                            name:'ایده‌پرداز' ,
                            status: 0
                        },
                        {
                            name:'تدریس کاربردی',
                            status: 0
                        },
                        {
                            name:'پر‌انرژی',
                            status: 0
                        },
                        {
                            name:'غیر قابل پیش بینی',
                            status: 0
                        },
                        {
                            name:'كلاس هاى جذاب',
                            status: 0
                        },
                        {
                            name:'دو بار وردار تا پاس شی',
                            status: 0
                        },
                        {
                            name:'سخت نمره میده',
                            status: 0
                        },
                        {
                            name:'کوییزهای رگباری',
                            status: 0
                        },
                        {
                            name:'سر کلاس نری افتادی',
                            status: 0
                        },
                        {
                            name:'کم حجم و مقوی',
                            status: 0
                        },
                        {
                            name:'انتظار مشارکت در کلاس دارد',
                            status: 0
                        },
                        {
                            name:'کلاس‌های بلند',
                            status: 0
                        },];
    // $scope.selectedTags = {};

    $scope.addTag = function(i){
        if($scope.allTags[i].status === 0 && $scope.selectedTagsCount<3){
            $scope.allTags[i].status = 1;
            $scope.selectedTagsCount++;
        }
        else if($scope.allTags[i].status === 1){
            $scope.allTags[i].status = 0;
            $scope.selectedTagsCount--;
        }

    };
    var getTags = function(){
        var selectedTags = [];
        for(i=0; i<$scope.allTags.length; i++){
            if($scope.allTags[i].status === 1){
                selectedTags.push($scope.allTags[i].name);
            }
        }
        return selectedTags;
    };
    $scope.getSubmitBtnTitle = function(){
        if($scope.submit===false)
            return 'ثبت امتیاز';
        return 'شما رای داده‌اید';
    };

    $scope.comment = "";
    $scope.applyComment = function(cmt){
        $scope.comment = cmt;
    };

    $scope.findCourse = true;
    $scope.canFindCourse = function(){
        $scope.findCourse = !$scope.findCourse;
    }
    var pushAlert = function(error){
        alert("هیچ گزینه‌ای برای " + error +" یافت نشد");
    };
    var pushCustomAlert = function(error){
        alert(error);
    };
    var checkErrors = function(course_name, selected_course){
         if($scope.findCourse == true){
            if(selected_course == undefined){
                pushCustomAlert("هیچ درسی انتخاب نکردی");
                return false;
            }
        }
        else{
            if(course_name == undefined){
                pushCustomAlert("هیچ درسی انتخاب نکردی");
                return false;
            }
        }

        if($scope.helpfulness == 0){
            pushAlert("دلسوزی");
            return false;
        }
        if($scope.easiness == 0){
            pushAlert("آسونی");
            return false;
        }
        if($scope.clarity == 0){
            pushAlert("قابل فهم بودن");
            return false;
        }
        if($scope.coolness == 0){
            pushAlert("باحالی");
            return false;
        }
        if($scope.useTextbook == 0){
            pushAlert("استفاده از کتاب");
            return false;
        }
        if($scope.attendance == 0){
            pushAlert("حضور غیاب");
            return false;
        }
        if($scope.comment == undefined || $scope.comment.length == 0){
            pushAlert("نظری");
            return false;
        }
        else if($scope.comment.length > 1000){
            pushCustomAlert("کامنت شما بیش از هزار کلمه است \n یکم کمتر بنویس لطفا :)");
            return false;
        }

        return true;
    };
    $scope.setResponse = function(response){
        $scope.response = response;
    };

    $scope.submitRate = function(cmt, course_name, selected_course){
        $scope.applyComment(cmt);
        if($scope.submit === false){

        if(!checkErrors(course_name, selected_course)){
            $scope.showModal = true;
            return false;
        }
        var rateData = {
            'id':$scope.id,
            'helpfulness':$scope.helpfulness,
            'easiness':$scope.easiness,
            'clarity':$scope.clarity,
            'coolness':$scope.coolness,
            'useTextbook':$scope.useTextbook,
            'attendance':$scope.attendance,
            'comment': $scope.comment,
            'tags':getTags(),
            'findCourse':$scope.findCourse,
            'courseName':course_name,
            'selectedCourse':selected_course,
            'response':$scope.response

        };
        console.log("RATE DATA");
        console.log(rateData);
        $http.post("/rate", rateData).success(function(data){
            $scope.submit = true;
            console.log("RESPONSE OF DATA");
            console.log(data);
            if(data.success){
                var main_result = $scope.$new();
                $controller('mainResult',{$scope : main_result });
                main_result.init($scope.id);
                console.log('after recieving data');
            }
        });

        return true;
    }

    };
    $scope.retVal = true;
    $scope.handleModal = function(retVal){
        if(retVal == false)
            $scope.showModal = true;
            retVal = true;
    };
    $scope.showModal = false;
    $scope.toggleModal = function(){
        $scope.showModal = !$scope.showModal;
    };

  }]);

app.directive('modal', function () {
    return {
      template: '<div class="modal fade">' +
          '<div class="modal-dialog">' +
            '<div class="modal-content">' +
              '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
                '<h4 class="modal-title">{{ title }}</h4>' +
              '</div>' +
              '<div class="modal-body" ng-transclude></div>' +
            '</div>' +
          '</div>' +
        '</div>',
      restrict: 'E',
      transclude: true,
      replace:true,
      scope:true,
      link: function postLink(scope, element, attrs) {
        scope.title = attrs.title;

        scope.$watch(attrs.visible, function(value){
          if(value == true)
            $(element).modal('show');
          else
            $(element).modal('hide');
        });

        $(element).on('shown.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = true;
          });
        });

        $(element).on('hidden.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = false;
          });
        });
      }
    };
  });

app.factory('Scopes', function ($rootScope) {
    var mem = {};

    return {
        store: function (key, value) {
            mem[key] = value;
        },
        get: function (key) {
            return mem[key];
        }
    };
});

app.factory('myService', function($http) {
  var myService = {
    async: function(id) {
      // $http returns a promise, which has a then function, which also returns a promise
      var promise = $http.get('/prof/getResults/' + id).then(function (response) {
        // The then function here is an opportunity to modify the response
        // The return value gets picked up by the then in the controller.
        return response.data;
      });
      // Return the promise to the controller
      return promise;
    }
  };
  return myService;
});

app.factory('reportComment', function($http) {
  var reportComment = {
    async: function(cmt_id) {
      // $http returns a promise, which has a then function, which also returns a promise
      var promise = $http.get('/report/' + cmt_id + '/').then(function (response) {
        // The then function here is an opportunity to modify the response

        // The return value gets picked up by the then in the controller.
        return response.data;
      });
      // Return the promise to the controller
      return promise;
    }
  };
  return reportComment;
});



var getCourses = function(data){
    // var data = [ { id: 4, text: 'wontfix' }];
    var select2_data = [];
    for(i = 0; i < data.length; i++){
        var temp = {id:data[i].name, text:data[i].name};
        select2_data.push(temp);
    }
    $("#js-example-data-array").select2({
        // placeholder: "Select a state",
        placeholder: "انتخاب کنید",
        // allowClear: true,
        // allowClear: true,
        dir: "rtl",
        data: select2_data
    });
};


// target element

// $(document).ready(function(){
//     var data = [ { id: 4, text: 'wontfix' }];

//     $("#js-example-data-array").select2({
//         data: data
//     });
// });


jQuery(document).ready(function($){
    $("#js-data-example-ajax").select2({
        ajax: {
            minimumInputLength: 3,
            url: "/search/asghar/",
            dataType: 'json',
            results: function (p) {
                return {results: p};
            },
        },
        formatResult: formatValues
    });
    function formatValues(data) {
        return data;
    }
    // browser window scroll (in pixels) after which the "back to top" link is shown
    var offset = 300,
    //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
        offset_opacity = 1200,
    //duration of the top scrolling animation (in ms)
        scroll_top_duration = 700,
    //grab the "back to top" link
        $back_to_top = $('.cd-top');

    //hide or show the "back to top" link
    $(window).scroll(function(){
        ( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
        if( $(this).scrollTop() > offset_opacity ) {
            $back_to_top.addClass('cd-fade-out');
        }
    });

    //smooth scroll to top
    $back_to_top.on('click', function(event){
        event.preventDefault();
        $('body,html').animate({
                scrollTop: 0 ,
            }, scroll_top_duration
        );
    });
});

