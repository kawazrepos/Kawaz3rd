$ ->
  # 添付素材用のポップアップを表示する
  showAttachmentPopup = ->
    $targetEditor = $(@).closest('.editor-control').prev('textarea')
    $dialog = $('#attachment-dialog').on('show.bs.modal', ->
      $input = $(@).find("input[type='text']")
      .hide()
      .fadeIn('fast', () ->
        $(@).focus()
      )
    )
    $dialog.data("$targetEditor", $targetEditor)
    $progress = $dialog.find(".progress-bar")
    $progress.text("")
    $progress("aria-valuenow", 0)
    $progress.css("width", "0%")

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
    $editor.data('mace', mace)

    # Mace buttons
    $control.find('.mace-indent').click(mace.indent.bind(mace, 1))
    $control.find('.mace-outdent').click(mace.outdent.bind(mace, 1))
    $control.find('.mace-heading-1').click(mace.heading.bind(mace, 1))
    $control.find('.mace-heading-2').click(mace.heading.bind(mace, 2))
    $control.find('.mace-heading-3').click(mace.heading.bind(mace, 3))
    $control.find('.mace-attachment').click(showAttachmentPopup)
  )

angular.kawaz.controller('AttachmentController', ($scope, $http, $upload) ->
  $scope.onFileSelect = ($files, $event) ->
    $dialog = $($event.target).closest('#attachment-dialog')
    $editor = $dialog.data("$targetEditor")
    mace = $editor.data("mace")
    $progress = $dialog.find(".progress-bar")

    setPercentage = (percent, label) ->
      label = label or "#{percent}%"
      $progress.attr("aria-valuenow", percent)
      $progress.css("width", "#{percent}%")
      $progress.text(label)

    for file in $files
      $scope.upload = $upload.upload(
        url: '/api/materials'
        data :
          "content_file": file
      ).progress((evt) ->
        percent = parseInt(100.0 * evt.loaded / evt.total)
        setPercentage(percent)

      ).success((data, status, headers, config) ->
        tag = data["tag"]
        mace.ace.insert(tag)
        setPercentage(100, "Completed")
      )
)