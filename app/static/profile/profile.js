
  
var app = angular.module('profile', []);
app.controller('rating', function(){
    var el = document.querySelector('#el');

    var currentRating = 0;

    var maxRating= 5;

    var callback = function(rating) { alert(rating); };

    var myRating = rating(el, currentRating, maxRating, callback);
});
app.controller('Comment', function($scope){
    var dict = {
        "coolness":{
            1:"آره",
            2:"نه"
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
    $scope.result_gen = function(key, id){
        // console.log(id)
        // console.log(key + " is : ")
        // console.log(dict[key][id.toString()])
        return dict[key][id.toString()];
    };
    $scope.calcPercent = function(val){
        var maximum = 5;
        return val/maximum*100;
    }
});


app.controller('mainResult', function(myService,$scope){
    var results = undefined;

    var save_json = function(res){
        console.log("SaveJSON");
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
                categories: ['مهربونی', 'خریت', 'حماقت'],
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
            tooltip: { enabled: false },
            series: [{    
                data: [{
                        
                        y: result.main_result.helpfulness.value,
                        // y: 9,
                        name: "Helpfulness",
                        color: result.main_result.helpfulness.color
                    }, {
                        
                        y: result.main_result.easiness.value,
                        // y: 8,
                        name: "Easiness",
                        color: result.main_result.easiness.color
                    },{
                       
                        y: result.main_result.clarity.value,
                        // y: 7,
                        name: "clarity",
                        color: result.main_result.clarity.color
                    }]
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
                enabled: false,
                text: result.name,
            },
            xAxis: {
                categories: ['Helpfulness', 'Easiness', 'clarity'],
                lineWidth: 0,
                minorGridLineWidth: 0,
                lineColor: 'transparent',
            },
            yAxis: {
                min: 0,
                max: 5,
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
            tooltip: { enabled: false },
            
            legend:{
                enabled: false,
            },
            credits: {
                enabled: false
            },
            series: [{    
                data: [{
                        
                        y: result.helpfulness.value,
                        // y: 9,
                        name: "Helpfulness",
                        color: result.helpfulness.color
                    }, {
                        
                        y: result.easiness.value,
                        // y: 8,
                        name: "Easiness",
                        color: result.easiness.color
                    },{
                       
                        y: result.clarity.value,
                        // y: 7,
                        name: "clarity",
                        color: result.clarity.color
                    }]
            }]
        });  
    };
    $scope.init = function(id){
        console.log("init");
        this.id = id;
        console.log(this.id);
        myService.async(this.id).then(function(d) {
            $scope.data = d;
            $scope.chart($scope.data);
            $scope.study_count = $scope.data.studies_result.length ;

            // $scope.study_chart($scope.data.studies_result[3],3)
            for(i = 0; i < $scope.data.studies_result.length; i++){
                // console.log(i);
                $scope.study_chart($scope.data.studies_result[i],i)
            }
            getCourses($scope.data.studies_result);

        });
    };
});

app.controller('MainCtrl', function ($scope,$http) {
    $scope.init = function(id){
        $scope.id = id;
        // $scope.comment = "";
    };
    // $scope.id = undefined;
    $scope.submit = false;
    var validateScore = function(score){
        if(score <= 6 && score > 0)
            return true;
        return false;
    };
    $scope.helpfulness = 0;
    $scope.setHelpfulness = function(score){
        console.log("helpfulness");
        if(validateScore(score)){
            $scope.helpfulness = score;
            console.log($scope.helpfulness);
        }
    };

    // $scope.comment = "";
    $scope.easiness = 0;
    $scope.setEasiness = function(score){
        console.log("easiness");

        if(validateScore(score)){
            $scope.easiness = score;
            console.log(score);
        }
    };
    $scope.clarity = 0;
    $scope.setClarity = function(score){
        console.log("clarity");

        if(validateScore(score)){
            $scope.clarity = score;
            console.log(score);
        }
    };

    $scope.coolness = 0;
    $scope.setCoolness = function(score){
        console.log("coolness");
        if(score<=2 && score>=0)
            $scope.coolness = score;
        console.log(score);
        console.log($scope.coolness);
    };

    $scope.useTextbook = 0;
    $scope.setUseTextbook = function(score){
        console.log("textbook");
        if(score<=2 && score>=0)
            $scope.useTextbook = score;
        console.log($scope.useTextbook);
    };

    $scope.attendance = 0;
    $scope.setAttendance = function(score){
        console.log("attendance");

        if(score<=3 && score>0){
            $scope.attendance = score;
            console.log($scope.attendance);
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
                            name:'به فکر پیشرفت و دلسوز', 
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
        console.log($scope.allTags);

    };
    var getTags = function(){
        var selectedTags = [];
        for(i=0; i<$scope.allTags.length; i++){
            if($scope.allTags[i].status === 1){
                selectedTags.push($scope.allTags[i].name);
            }
        }
        console.log(selectedTags);
        return selectedTags;
    };
    $scope.getSubmitBtnTitle = function(){
        if($scope.submit===false)
            return 'ثبت امتیاز';
        return 'شما رای داده‌اید';
    };

    $scope.comment = "";
    $scope.applyComment = function(cmt){
        console.log(cmt);
        $scope.comment = cmt;
        console.log("this is applyComment");
    };

    $scope.findCourse = true;
    $scope.canFindCourse = function(){
        $scope.findCourse = !$scope.findCourse;
    }

    $scope.submitRate = function(cmt, course_name, selected_course){
        $scope.applyComment(cmt);
        if($scope.submit === false){
            $scope.submit = true;
        console.log("course name");
        console.log(course_name);
        console.log("find course");
        console.log($scope.findCourse);
        console.log("selected course -->" + selected_course);
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
            'selectedCourse':selected_course
        };
        $http.post("/rate", rateData).success(function(data){
            console.log(data);
        });
    }

    };

    $scope.showModal = false;
    // this.data = {};
    $scope.toggleModal = function(){
        $scope.showModal = !$scope.showModal;
    };

  });

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


app.factory('myService', function($http) {
  var myService = {
    async: function(id) {
      // $http returns a promise, which has a then function, which also returns a promise
      var promise = $http.get('/prof/getResults/' + id).then(function (response) {
        // The then function here is an opportunity to modify the response
        console.log(response);
        // The return value gets picked up by the then in the controller.
        return response.data;
      });
      // Return the promise to the controller
      return promise;
    }
  };
  return myService;
});


var getCourses = function(data){
    // var data = [ { id: 4, text: 'wontfix' }];
    console.log("getCourses");
    console.log(data);
    var select2_data = [];
    for(i = 0; i < data.length; i++){
        var temp = {id:data[i].name, text:data[i].name};
        select2_data.push(temp);
    }
    $("#js-example-data-array").select2({
        // placeholder: "Select a state",
        placeholder: "انتخاب کنید",
        allowClear: true,
        // allowClear: true,
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
  