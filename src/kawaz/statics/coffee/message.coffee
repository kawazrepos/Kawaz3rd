$ ->
  $('.message').each(() ->
    message = $(@)
    message.hide()
    tag = message.attr('message-tag')
    message = message.text()

    # ref : http://www.jqueryrain.com/?SlxLijWt
    $.bootstrapGrowl(message,
      type: tag
      align: 'center'
      width: 'auto'
    )
  )
