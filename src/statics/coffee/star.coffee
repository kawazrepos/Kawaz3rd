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
  $(@).hide()
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

  stars = {}
  # 同じユーザーのスターについてはまとめる
  $stars = $(@).find('.star')
  # コメントを持っていないスター
  $stars.each(() ->
    authorId = $(@).attr("star-author-id")
    quote = $(@).attr("star-quote")
    # そのユーザーIDに関する辞書がなければ初期化
    stars[authorId] ?= {count: 0, comments: []}
    if quote
      stars[authorId]['comments'].push($(@))
    else
      # quoteが付いてないスターの数だけカウント
      ++stars[authorId]['count']
      stars[authorId]['$star'] ?= $(@)
  )
  $container = $(@).find('.star-list')
  $container.empty()
  for authorId, dict of stars
    $wrapper = $("<li>").addClass("star-wrapper")
    # コメント付きのスター追加
    for $comment in dict['comments']
      $wrapper.append($comment)
    # コメント無しのスター+カウント追加
    if dict['$star']
      $wrapper.append(dict['$star'])
    if dict['count'] > 1
      $wrapper.append($("<span>").addClass("star-count").text(dict['count']))
    $container.append($wrapper)


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
  $(@).show()

)