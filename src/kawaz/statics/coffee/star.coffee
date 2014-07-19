angular.kawaz.controller('StarController', ($scope, $http) ->

  $scope.fetchStars = ->
    $http.get($scope.endpoint, {}).success( (data, status, headers, config) ->
      $scope.stars = angular.fromJson(data)
    )

  $scope.addStar = (e) ->
    e.preventDefault()
    regex = /([a-z_]+)=(\d+)/g
    params = $scope.endpoint.match(regex)

    quote = document.getSelection().toString()

    # URLパラメータをがんばってObjectに変換している
    data =
      quote: quote
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

  $scope.showPopup = ((e, star) ->
    star.visible = true
    $scope.popupPosition =
      left: e.pageX + 12
      top: e.pageY + 12
  )

  $scope.deleteStar = (star) ->
    console.log star
    pk = star.id
    params =
      pk: pk
    if confirm("スターを削除します。よろしいですか？")
      $http.delete("/api/stars/#{pk}.json", params).success( (data) ->
        index = $scope.stars.indexOf(star)
        $scope.stars.splice(index, 1)
      )


)