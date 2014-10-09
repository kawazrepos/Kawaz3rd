$ ->
  # .post-linkが付いたリンクをクリックしたときにPOSTを送ります
  $('.post-link').click(->
    url = $(@).attr('href')
    # もし、confirm-messageというプロパティがあれば、確認メッセージを出します
    message = $(@).attr('confirm-message')

    $form = $(@).find('form')
    if not message or window.confirm(message)
      $form.attr('action', url).submit()

    return false
  )
