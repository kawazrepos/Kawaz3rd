# 後で widget 化

$ ->
  # 添付素材用のポップアップを表示する
  showAttachmentPopup = ->
    console.log($('#attachment-dialog'))
    $dialog = $('#attachment-dialog').on('show.bs.modal', ->
      console.log("huga")
      $input = $(@).find("input[type='text']")
      .hide()
      .fadeIn('fast', () ->
        $(@).focus()
      )
    )

  $editors = $('.mace-editor')

  $editors = $editors.each(->
    # textarea を隠す
    $editor = $(@).hide()

    # 親要素に div 要素追加
    $parent = $editor.parent()
    $wrapper = $('<div class="edit-area">').text($editor.val())
           .css('min-height', '400px')
    $control = $parent.find('.editor-control')
    $parent.append($control, $wrapper)

    # Mace を組み込む
    mace = new Mace($wrapper.get(0))
    # 入力内容を textarea に反映
    mace.ace.on('change', ->
      $editor.val(mace.value)
    )

    # Mace buttons
    $control.find('.mace-indent').click(mace.indent.bind(mace, 1))
    $control.find('.mace-outdent').click(mace.outdent.bind(mace, 1))
    $control.find('.mace-heading-1').click(mace.heading.bind(mace, 1))
    $control.find('.mace-heading-2').click(mace.heading.bind(mace, 2))
    $control.find('.mace-heading-3').click(mace.heading.bind(mace, 3))
    $control.find('.mace-attachment').click(showAttachmentPopup)
  )
