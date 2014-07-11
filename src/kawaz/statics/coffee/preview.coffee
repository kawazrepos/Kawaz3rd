angular.kawaz.controller('FormController', ($scope, $http) ->

  $scope.preview = ""

  # タブの切り替え
  $scope.toggleEditor = ($event) ->
    $event.preventDefault()
    $($event.target).tab 'show'
    false

  $scope.togglePreview = ($event, previewURL) ->
    $event.preventDefault()
    $($event.target).tab 'show'

    $form = $('#editor-main form')
    dump = $form.serialize()

    # Preview用ページを取得する:
    $http.get("#{previewURL}?#{dump}").success( (data, status, headers, config) ->
      $scope.preview = data
    )
    false

)
