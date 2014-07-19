# Angular Applicationをグローバルに取得できるようにします
angular.kawaz = angular.module('kawaz', ['ngSanitize'])
.config(($interpolateProvider, $httpProvider) ->
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
)
