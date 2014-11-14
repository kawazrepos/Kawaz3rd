angular.kawaz.controller('FormController', ($scope, $http, $sce) ->

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
    # jQuery.serializeObjectでformをJSON化している
    dump = $form.serializeObject()

    $scope.showPreview = true

    # Preview用ページを取得する:
    $http.post(previewURL, dump).success( (data, status, headers, config) ->
      # http://stackoverflow.com/questions/20165780/insert-an-iframe-into-page-dynamically-in-angularjs
      $scope.preview = $sce.trustAsHtml(data)
    )
    false
)
