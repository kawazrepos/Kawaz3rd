# DjangoのCSRF protectionを回避するため、Cookieのcsrfトークンを
# リクエストヘッダーに追加している
# このコードをCoffeeScriptに移植しただけ
# Ref : https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/#ajax
$ ->
  csrftoken = $.cookie('csrftoken')

  csrfSafeMethod = (method) ->
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

  $.ajaxSetup(
    beforeSend: (xhr, settings) ->
      if !csrfSafeMethod(settings.type) and not @crossDomain
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
  )

$('.star-container').each(->
  $button = $(@).find('.add-star-button')
  endpoint = $(@).attr('star-endpoint')

  $starContainer = $(@).find('.star-body-col ul')

  # スター追加ボタンが押されたとき
  $button.click((e) ->
    # 現在のカーソルの選択範囲をquoteにする
    quote = document.getSelection().toString()

    # URLパラメータをがんばってObjectに変換している
    # url?object_id=1&content_type=1という形式の文字列が$scope.endpointに入っていて
    # URLエンコードなどはされていない状態で渡される
    # パラメーター部分は必ずPKである整数値が入っているためデコードを考慮していない
    querystring = endpoint.split('?')[1] or ''
    data =
      quote: quote
    querystring.split('&').forEach((param) ->
      bits = param.split('=')
      key = decodeURIComponent(bits[0])
      value = decodeURIComponent(bits[1])
      data[key] = value
    )

    $.post(endpoint, data)
    .done((data) ->
      html = data['html']
      $star = $(html)
      $starContainer.append($star)
      $star.hide().fadeIn( ->
        $star.attr('title', data['tooltip'])
      )
    ).fail( () ->
      alert("スターを上手く付けられませんでした")
    )
  )

  # スターが15個以上付いてるとき、畳む
  $readmore = $(@).find('.star-read-more')
  $stars = $(@).find('.star')
  starCount = $stars.size()
  $readmore.find('.text').text(starCount)
  maxStarCount = 15
  if starCount < maxStarCount
    $readmore.hide()
  else
    $invisible = $stars[maxStarCount...]
    $wrapper = $('<div>')
    $invisible.remove()
    $wrapper.append($invisible)
    $starContainer.append($wrapper)
    $wrapper.hide()
    $readmore.show()
    $readmore.click(() ->
      $wrapper.toggle()
      $(@).hide()
    )

  # スターにマウスオーバーしたときに削除ボタンをトグルする
  # Note: 動的に追加されたスターにも適応するためにon(delegate)を利用している
  $(@).on('mouseover', '.star', ->
    $(@).find('.star-remove').show()
  )
  $(@).on('mouseout', '.star', ->
    $(@).find('.star-remove').hide()
  )

  # hoverしたときのtooltipを登録する
  # Note:
  # `selector`オプションを加えることで$.onでbindできるため
  # あとから追加されたStarについてもtooltipが表示される
  $(@).tooltip(
    selector: '.star'
  )

  # スターの削除ボタンを押したとき
  $(@).on('click', '.star-remove', ->
    $star = $(@).closest('.star')
    pk = $star.attr('star-id')
    if confirm("削除します。よろしいですか？")
      $.ajax({type: 'DELETE', url: "/api/stars/#{pk}.json"})
      .done( (data) ->
        $star.fadeOut(() ->
          $(@).remove()
        )
      )
      .fail(->
        alert("スターの削除に失敗しました")
      )
    return false
  )

)