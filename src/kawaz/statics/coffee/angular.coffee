# Angular Applicationをグローバルに取得できるようにします
angular.kawaz = angular.module('kawaz', ['ngSanitize'])
       .config(($interpolateProvider, $httpProvider) ->
  # デフォルトのSymbol {{ }}はDjangoのテンプレートエンジンと衝突するため
  # [[ angularVariable ]]で展開できるようにしている
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
  # Djangoのcsrf対応のためにデフォルトの$httpの挙動を変更している
  # http://stackoverflow.com/questions/18335162/xsrf-headers-not-being-set-in-angularjs
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
)
