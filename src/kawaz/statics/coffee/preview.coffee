angular.kawaz.controller('FormController', ($scope, $http) ->

  # Previewに表示する文字列
  $scope.preview = ""
  # Previewタブが表示状態かどうか
  $scope.showPreview = false

  # Editorタブが押されたとき
  $scope.toggleEditor = ($event) ->
    $event.preventDefault()
    $($event.target).tab 'show'
    $scope.showPreview = false
    false

  # Previewタブが押されたとき
  $scope.togglePreview = ($event, previewURL) ->
    $event.preventDefault()
    $($event.target).tab 'show'

    # これ、jQueryを使わずに上手くできないか
    $form = $('#editor-main form')
    dump = $form.serialize()

    $scope.showPreview = true

    # Preview用ページを取得する:
    $http.get("#{previewURL}?#{dump}").success( (data, status, headers, config) ->
      $scope.preview = data
    )
    false

)
