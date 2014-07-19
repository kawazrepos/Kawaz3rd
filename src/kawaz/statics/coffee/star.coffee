angular.kawaz.controller('StarController', ($scope, $http) ->

  $scope.fetchStars = ->
    $http.get($scope.endpoint, {}).success( (data, status, headers, config) ->
      $scope.stars = angular.fromJson(data)
    )

  $scope.addStar = (e) ->
    e.preventDefault()
    regex = /([a-z_]+)=(\d+)/g
    params = $scope.endpoint.match(regex)

    # URLパラメータをがんばってObjectに変換している
    data = {}
    $(params).each((index, param) ->
      bits = param.split('=')
      key = bits[0]
      value = bits[1]
      data[key] = value
    )

    $http.post($scope.endpoint, data).success((star) ->
      # response
      $scope.stars.push(star)
    )

)