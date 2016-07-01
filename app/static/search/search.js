var app = angular.module('search', []);
app.controller('searchBox',function($scope, $http, $timeout){
	// $scope.search_result = null;
	$scope.keyword = null;
	this.focus = false;
	this.setFocusTrue = function(){
		this.focus = true;
		// alert("true");
	};
	this.setFocusFalse = function(){
		this.focus = false;
		// alert("false");
	};
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

	function nextpage() {
		// $("#logo").hide();
		// $("#search-place").hide();
        //
		// $("#search-box").animate({"top":'-=60%'},1000);
		// $("#arrow-down").hide();
		// $("#head").delay(800).fadeIn();
		// $("#detail").delay(800).fadeIn();
		// $("#tiser").play();

	}
