$ ->
  $containers = $('.formset')
  # 1ページ内に複数のformsetがある可能性があるのでformsetごとに処理をする
  $containers.each(->
    $container = $(@)
    $panelContainer = $container.find('.panel-container')
    $addButton = $container.find('.formset-add')
    $template = $container.find('.panel-formset:last-child').clone()
    $template.find("input[type='checkbox']").remove()

    # prefix attributeが設定されてるはず
    prefix = $container.attr('prefix')
    unless prefix?
      # rowにprefixが設定されてなかったらHTMLの構造がおかしいので警告を出す
      throw new Exception("formsetのprefixが設定されていません。")

    # 削除ボタン
    # ボタンが追加されても動くようにonでbindしている
    $container.on('click', '.formset-remove', ->
      $row = $(@).closest('.panel-formset')
      $deleteField = $row.find("[id$='DELETE']")
      # 削除フィールドが存在しているrowはすでに登録済みの奴
      isRegistered = $deleteField.size() > 0
      console.log isRegistered
      $row.fadeOut ->
        if isRegistered
          # 登録済みの場合、削除フィールドにcheckを入れて非表示にするだけ
          $deleteField.prop('checked', true)
        else
          # 登録していないとき、POSTする必要はないからフォームごと消してしまう
          $(@).remove()
        updateTotalForms()
      false
    )
    # すでにあるフォームの数をcurrentUniqueIDにして、フォームを追加するごとにincrement
    currentUniqueID = $container.find('.panel-formset').size()

    maxNumForms = parseInt($("#id_#{prefix}-MAX_NUM_FORMS").val(), 10)

    # deleteボタンを消しておく
    $container.find("#id_#{prefix}-DELETE").hide()

    # 追加ボタン
    $addButton.click(->
      formCount = $container.find('.panel-formset').size()
      # フォームの最大値以上だったらもう追加しない
      if formCount >= maxNumForms
        return false
      $newRow = $template.clone()
      $panelContainer.append $newRow

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

      $newRow.hide().fadeIn()

      updateTotalForms()

      false
    )

    updateTotalForms = ->
      $totalForms = $("#id_#{prefix}-TOTAL_FORMS")
      formCount = $container.find('.panel-formset').size()
      $totalForms.val(formCount)
  )

$ ->
  # datetimepickerを表示させる
  $("[type='datetime']").datetimepicker(
    'format' : 'Y-m-d H:i'
    'lang' : 'ja'
  )
  # datepickerを表示させる
  $("[type='date']").datetimepicker(
    'timepicker' : false
    'format' : 'Y-m-d'
    'lang' : 'ja'
  ).prop('type', 'text')
  # Google Chrome標準のdate pickerがウザいので殺している
  # http://stackoverflow.com/questions/11270675/how-can-i-disable-the-new-chrome-html5-date-input


$ ->
  # Profileのアカウント登録用セレクトボックスにサービスアイコンを表示する
  updateIcon = (target) ->
    $option = $(target).find('option:selected')
    url = $option.attr('icon-url')
    console.log(url)
    $(target).css('background-image', "url(#{url})")
  $('.serviceselectwidget').change(->
    updateIcon(@)
  )
  $.each($('.serviceselectwidget'), (i, v) ->
    updateIcon(v)
  )

