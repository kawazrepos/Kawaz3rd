# Star表示、操作用のAngularJSコントローラー
#
#
angular.kawaz.controller('StarController', ($scope, $http) ->

  # 取得した全てのスター
  $scope.stars = []
  # 実際に表示されてるスター
  $scope.visibleStars = []
  # スターの初期最大表示数
  $scope.starVisibleThreshold = 20
  # もっと読むカウント
  $scope.readMoreCount = 0
  # もっと読むが開いてるフラグ
  $scope.isReadMoreOpened = false

  # スター一覧を取得する
  $scope.fetchStars = ->
    $http.get($scope.endpoint, {}).success( (data, status, headers, config) ->
      $scope.stars = angular.fromJson(data)
    )

  # スターを追加ボタンが押されたとき
  #
  # @param [Event] e
  #
  $scope.addStar = (e) ->
    e.preventDefault()

    # 現在のカーソルの選択範囲をquoteにする
    quote = document.getSelection().toString()

    # URLパラメータをがんばってObjectに変換している
    # url?object_id=1&content_type=1みたいなのが$scope.endpointに入ってるはず
    querystring = $scope.endpoint.split('?')[1] or ''
    data =
      quote: quote
    querystring.split('&').forEach((param) ->
      bits = param.split('=')
      key = decodeURIComponent(bits[0])
      value = decodeURIComponent(bits[1])
      data[key] = value
    )

    $http.post($scope.endpoint, data).success((star) ->
      $scope.stars.push(star)
    )

  # starがマウスオーバーされたとき
  #
  # @param [Event] e
  # @param [Object] star StarのObject
  #
  $scope.showPopup = ((e, star) ->
    star.visible = true
    $scope.popupPosition =
      left: e.pageX + 12
      top: e.pageY + 12
  )

  # 削除ボタンが押されたとき
  #
  # @param [Object] star StarのObject
  #
  $scope.deleteStar = (star) ->
    pk = star.id
    params =
      pk: pk
    if confirm("スターを削除します。よろしいですか？")
      $http.delete("/api/stars/#{pk}.json", params).success( (data) ->
        index = $scope.stars.indexOf(star)
        $scope.stars.splice(index, 1)
      )

  # 実際に表示するスターを更新する
  updateVisibleStars = ->
    starCount = $scope.stars?.length
    # スターが一定数以上になったときに畳む
    if starCount > $scope.starVisibleThreshold
      $scope.readMoreCount = starCount - $scope.starVisibleThreshold
      if $scope.isReadMoreOpened
        # 開いてたらスターを全て表示
        $scope.visibleStars = $scope.stars
      else
        # そうじゃなきゃ切り詰めて表示
        $scope.visibleStars = $scope.stars[0...$scope.starVisibleThreshold]
    else
      $scope.visibleStars = $scope.stars

  # starsの更新を監視する
  $scope.$watchCollection("stars", updateVisibleStars)

  # readMoreが押されたとき
  $scope.openReadMore = ->
    $scope.isReadMoreOpened = true
    updateVisibleStars()

)
