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
    # ダイアログはページ中に1つだが、フォームは複数個ある可能性があるので
    # 現在、どのMace Editorを編集しているかを保存している
    $dialog.data("$targetEditor", $targetEditor)

    # プログレスバーを0%にリセットしている
    $progress = $dialog.find(".progress-bar")
    $progress.text("")
    $progress.attr("aria-valuenow", 0)
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
    # Maceを.mace-editorに紐付けておく
    $editor.data('mace', mace)

    # Mace buttons
    $control.find('.mace-indent').click(mace.indent.bind(mace, 1))
    $control.find('.mace-outdent').click(mace.outdent.bind(mace, 1))
    $control.find('.mace-heading-1').click(mace.heading.bind(mace, 1))
    $control.find('.mace-heading-2').click(mace.heading.bind(mace, 2))
    $control.find('.mace-heading-3').click(mace.heading.bind(mace, 3))
    # ["item 1"] リスト初期化用の配列なので、無くても良いです
    $control.find('.mace-list').click(mace.list.bind(mace, '-', ['Item']))
    $control.find('.mace-numeric-list').click(mace.list.bind(mace, 1, ['Iten']))
    $control.find('.mace-bold').click(mace.bold.bind(mace, '*', '太字'))
    $control.find('.mace-italic').click(mace.italic.bind(mace, '*', 'イタリック'))
    $control.find('.mace-line').click(mace.line.bind(mace, '*'))
    $control.find('.mace-code').click(->
      mace.code('ソースコード')
    )
    $control.find('.mace-quote').click(->
      mace.quote('引用')
    )
    $control.find('.mace-image').click(->
      url = prompt('画像の URL を入力')
      # 最後の引数の true は画像であることを示す
      mace.link(url, '画像', 'タイトル', true)
    )
    $control.find('.mace-link').click(->
      url = prompt('URL を入力')
      mace.link(url, 'リンク')
    )
    $control.find('.mace-attachment').click(showAttachmentPopup)
  )

angular.kawaz.controller('AttachmentController', ($scope, $http, $upload) ->
  $scope.onFileSelect = ($files, $event) ->
    # ダイアログを取り出す
    $dialog = $($event.target).closest('#attachment-dialog')
    # 編集中のエディタを取り出す
    $editor = $dialog.data("$targetEditor")
    mace = $editor.data("mace")
    $progress = $dialog.find(".progress-bar")

    # プログレスバーを変更する便利関数
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
        # レスポンスから "{attachments:<slug>}"みたいな文字列を取り出して、エディタ中に挿入する
        tag = data["tag"]
        mace.ace.insert(tag)
        setPercentage(100, "Completed")
      ).error(() ->
        alert("アップロードエラーが発生しました。管理者に問い合わせてください")
        setPercentage(0, "Error")
      )
)