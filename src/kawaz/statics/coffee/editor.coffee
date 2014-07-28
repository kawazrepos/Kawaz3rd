# 後で widget 化
control = '''
<div class="editor-control">
  <div class="btn-group btn-group-sm">
    <div class="mace-outdent btn btn-default">
      <span class="glyphicon glyphicon-indent-right"></span>
    </div>
    <div class="mace-indent btn btn-default">
      <span class="glyphicon glyphicon-indent-left"></span>
    </div>
    <div class="mace-heading-1 btn btn-default">
      <span>H1</span>
    </div>
    <div class="mace-heading-2 btn btn-default">
      <span>H2</span>
    </div>
    <div class="mace-heading-3 btn btn-default">
      <span>H3</span>
    </div>
  </div>
</div>
'''

$ ->
  $editors = $('.mace-editor')

  $editors = $editors.each(->
    # textarea を隠す
    $editor = $(@).hide()

    # 親要素に div 要素追加
    $parent = $editor.parent()
    $wrapper = $('<div class="edit-area">').text($editor.val())
           .css('min-height', '100px')
    $control = $(control)
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
  )
