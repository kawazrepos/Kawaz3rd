# 後で widget 化
control = '''
<div class="editor-control">
  <div class="btn-group btn-group-sm">
    <div class="mace-indent btn btn-default">
      <span class="glyphicon glyphicon-indent-left"></span>
    </div>
    <div class="mace-outdent btn btn-default">
      <span class="glyphicon glyphicon-indent-right"></span>
    </div>
    <div class="mace-heading btn-group btn-group-sm">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
        Heading
        <span class="caret"></span>
      </button>
      <ul class="dropdown-menu">
        <li><a href="#">h1</a></li>
        <li><a href="#">h2</a></li>
        <li><a href="#">h3</a></li>
        <li><a href="#">h4</a></li>
        <li><a href="#">h5</a></li>
        <li><a href="#">h6</a></li>
      </ul>
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
    $heading = $control.find('.mace-heading li')
    $heading.click(() ->
      level = $heading.index(@) + 1
      mace.heading(level)
      # inactivate
      $(@).parent().click()
      return false
    )
  )
