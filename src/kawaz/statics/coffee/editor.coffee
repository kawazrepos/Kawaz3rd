$ ->
  # エディタを設置する textarea の id を列挙する
  $editors = $('#id_body, #id_description, #id_remarks')

  $editors = $editors.each(->
    # textarea を隠す
    $textarea = $(@)
    $textarea.hide()

    # 親要素に div 要素追加
    $parent = $textarea.parent()
    $parent.append(document.createElement('div'))

    # 追加した div 要素を editor として設定
    $editor = $parent.find('div')
    $editor.text($textarea.val())
           .css('min-height', '100px')
    
    # Mace を組み込む
    mace = new Mace($editor.get(0))
    # 入力内容を textarea に反映
    mace.ace.on('change', ->
      $textarea.val(mace.value)
    )
  )
