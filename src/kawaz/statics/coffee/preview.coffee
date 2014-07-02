$ ->
  $previewTab = $('.preview-tab')
  $tabs = $(".nav-tabs li a")
  url = $('#editor-preview').attr('preview-url')
  $previewContainer = $('#editor-preview')

  $tabs.click( (e) ->
    e.preventDefault()
    $(@).tab('show')
  )

  $previewTab.click( ->
    $previewContainer.empty()
    $form = $('#editor-main form')
    dump = $form.serializeArray()

    $.get(url, dump, (data) ->
      $preview = $(data)
      $previewContainer.append($preview)
    )
  )