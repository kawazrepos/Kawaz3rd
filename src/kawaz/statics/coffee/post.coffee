$ ->
  # .post-linkが付いたリンクをクリックしたときにPOSTを送ります
  $('.post-link').click(->
    csrfToken = $(@).attr('csrf-token')
    url = $(@).attr('href')
    $form = $(@).find('form')
    $form.attr('action', url).submit()
    console.log($form)
    return false
  )