$ ->
  $containers = $('.formset')
  # 1ページ内に複数のformsetがある可能性があるのでformsetごとに処理をする
  $containers.each(->
    $container = $(@)
    $table = $container.find('table')
    $addButton = $container.find('.formset-add')
    $formsetRow = $container.find('.formset-row:last-child').clone()

    # prefix attributeが設定されてるはず
    prefix = $container.attr('prefix')
    if not prefix?
      # rowにprefixが設定されてなかったらHTMLの構造がおかしいので警告を出す
      alert("formsetのprefixが設定されていません。")

    # 削除ボタン
    # ボタンが追加されても動くようにonでbindしている
    $table.on('click', '.formset-remove', ->
      $row = $(@).closest('.formset-row')
      $deleteField = $row.find("[id$='DELETE']")
      # 削除フィールドが存在しているrowはすでに登録済みの奴
      isRegistered = $deleteField.size() > 0
      $row.fadeOut ->
        if isRegistered
          $deleteField.attr('checked', true)
        else
          $(@).remove()
        updateTotalForms()
      false
    )
    # すでにあるフォームの数をcurrentUniqueIDにして、フォームを追加するごとにincrement
    currentUniqueID = $container.find('.formset-row').size()

    maxNumForms = parseInt($("#id_#{prefix}-MAX_NUM_FORMS").val(), 10)

    # deleteボタンを消しておく
    $deleteField = $container.find("[id$='DELETE']")
    $deleteField.hide()

    # 追加ボタン
    $addButton.click(->
      formCount = $container.find('.formset-row').size()
      # フォームの最大値以上だったらもう追加しない
      if formCount >= maxNumForms
        false
      $newRow = $formsetRow.clone()
      $table.append $newRow

      # 特定のattributeをユニークな物に変更するメソッド
      setNewAttr = (attrName) ->
        $newRow.find("[#{attrName}*='#{prefix}']").each(->
          name = $(@).attr(attrName)
          # "#{prefix}-${id}-#{fieldName}"というvalueになっているはず
          elems = name.split('-')
          elems[1] = currentUniqueID
          newValue = elems.join('-')
          $(@).attr(attrName, newValue)
        )
      # ID要素、name要素をユニークな物に変更する
      setNewAttr('id')
      setNewAttr('name')

      ++currentUniqueID

      $newRow.hide()
      $newRow.fadeIn()
      $newRow.find()

      updateTotalForms()

      false
    )

    updateTotalForms = ->
      $totalForms = $("#id_#{prefix}-TOTAL_FORMS")
      formCount = $container.find('.formset-row').size()
      $totalForms.val("#{formCount}")
  )
