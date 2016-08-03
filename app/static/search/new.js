var app = angular.module('search', []);
app.controller('searchBox',function($scope, $http, $timeout, $element){
    // $scope.search_result = null;
    $scope.keyword = null;
    this.focus = false;
    this.onResult = false;
    this.counter = 0;
    this.setOnResult = function(){
        console.log("onResult");
        this.onResult = true;
        this.focus = true;
        console.log("	onResutl: " + this.onResult);
        console.log("	focus: " + this.focus);
    }
    this.setFocusTrue = function(){
        // console.log(this.focus);
        console.log("trueeee");
        if(this.counter != 0)
            this.onResult = false;
        this.counter = 1;
        this.focus = true;
        console.log("	onResutl: " + this.onResult);
        console.log("	focus: " + this.focus);
        // alert("true");
    };
    this.setFocusFalse = function(){
        // console.log(this.focus);
        // console.log(item);
        // console.log(angular.element(item)[0].data('id'));
        console.log("falseeeee");
        this.focus = false;
        console.log("	onResutl: " + this.onResult);
        console.log("	focus: " + this.focus);
        // alert("false");
    };

    this.flipFocus = function(){
        this.focus = !this.focus;
    }
    this.prof_url_for = function(id){
        // console.log("id"+id);
        return Flask.url_for("profile.prof", {"id":id});
    }
    $scope.checkResult = function(profs, faculties, unis){
        console.log()
        return !profs && !faculties && !unis;
    }
    $scope.search = function() {
        if($scope.keyword.length == 0)
            $scope.search_result = null;
        if($scope.keyword.length > 2){
            $timeout(function(){$http.get('/search/asghar/'+ $scope.keyword)
                .then(function(result){
                    $scope.search_result = result;
                })}, 500);
        }
        // console.log($scope.search_result);
    }
    // $scope.prof = $scope.search_result.data.profs != null;
    // $scope.uni = $scope.search_result.data.unis != null;
    // $scope.fac = $scope.search_result.data.faculties != null;
    // console.log("akbar is dirty");
});


    // alert("lksdfl");


