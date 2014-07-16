$ ->
  # エディタを設置する textarea の id を列挙する
  $editors = $('.mace-editor')

  $editors = $editors.each(->
    # textarea を隠す
    $editor = $(@).hide()

    # 親要素に div 要素追加
    $parent = $editor.parent()
    $wrapper = $('<div>').text($editor.val())
           .css('min-height', '100px')
    $parent.append($wrapper)

    # Mace を組み込む
    mace = new Mace($wrapper.get(0))
    # 入力内容を textarea に反映
    mace.ace.on('change', ->
      $editor.val(mace.value)
    )
  )
