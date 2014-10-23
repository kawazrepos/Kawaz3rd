# Socialボタン設置用スクリプト

prepareHatenaBookmarkButton = ->
  # はてなブックマークボタンを設置します
  $hb = $('.hatena-bookmark-button')
  bookmark = "http://b.hatena.ne.jp/entry/#{location.href}"
  $hb.attr('href', bookmark)

prepareFaceBookButton = ->
  # FaceBookのLike!ボタンを設置します
  $fb = $('.fb-like')
  $fb.attr('data-href', location.href)

prepareSocialButtons = ->
  # 全てのソーシャルボタンを設置します
  prepareFaceBookButton()
  prepareHatenaBookmarkButton()

$ ->
  prepareSocialButtons()
