# Socialボタン設置用スクリプト
$ ->
  # はてなブックマークボタン
  $hb = $('a.hb-button')
  bookmark = "http://b.hatena.ne.jp/entry/{location.href}"
  $hb.attr('href', bookmark)
  # Facebook いいね
  $fb = $('.fb-like')
  $fb.attr('data-href', location.href)