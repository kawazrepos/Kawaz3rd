# ブログカテゴリー追加用のスクリプト
angular.kawaz.controller('BlogCategoryController', ($scope, $http) ->
  # カテゴリ選択用のフィールド
  $categorySelect = $('#id_category')
  $addButton = $(".blog-category-add-button").parent()
  $addButton.remove()
  $categorySelect.after($addButton)

  $dialog = $('#blog-category-dialog').on('show.bs.modal', ->
    $input = $(@).find("input[type='text']")
    .hide()
    .fadeIn('fast', () ->
      $(@).focus()
    )
  )

  # カテゴリーを作成
  $scope.createCategory = () ->
    label = $scope.categoryLabel
    params =
      label: label
    $http.post($scope.endpoint, params).success((data) ->
      $select = $('<option>').val(data.id).append(data.label)
      # 追加したカテゴリをカテゴリ一覧に加える
      $categorySelect.append($select)
      # 追加したカテゴリをカテゴリ一覧の中から選択状態にする
      $categorySelect.val(data.id)
      # ボックスを閉じる
      $dialog.modal('hide')
    ).error((data, status, headers, config) ->
      # ボックスを閉じる
      $dialog.modal('hide')
      alert("カテゴリの作成に失敗しました。同名のカテゴリがないかを確認してください")
    )
)
