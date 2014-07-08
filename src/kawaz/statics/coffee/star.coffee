kawaz = angular.module('kawaz', []).config(($interpolateProvider) ->
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
)

kawaz.controller('StarController', ($scope, $http) ->
  $scope.fetchStars = ->
    $http.get($scope.endpoint, {}).success( (data, status, headers, config) ->
      $scope.stars = angular.fromJson(data)
      console.log($scope.stars)
    )
)