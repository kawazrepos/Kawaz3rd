# ブログカテゴリー追加用のスクリプト
angular.kawaz.controller('BlogCategoryController', ($scope, $http) ->
  $dialogButton = $('.blog-category-add-button')
  dialogSelector = $dialogButton.attr('href')
  $dialogButton.fancybox(
    minHeight: '0px'
    afterShow: () ->
      # fancybox表示後にフォーカスを当てる
      $input = $(dialogSelector).find("input[type='text']")
      $input.focus()
  )

  $scope.isShowDialog = false
  $categorySelect = $('#id_category')

  $scope.createCategory = () ->
    label = $scope.categoryLabel
    params =
      label: label
    $http.post($scope.endpoint, params)
    .success((data) ->
      $select = $('<option>').val(data.id).append(data.label)
      $categorySelect.append($select)
      # セレクトさせる
      $categorySelect.val(data.id)
      # ボックスを閉じる
      $.fancybox.close()
    )
    .error((data, status, headers, config) ->
      alert("カテゴリの登録でエラーが発生しました")
      $.fancybox.close()
    )
)
