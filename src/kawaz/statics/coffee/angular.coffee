# Angular Applicationをグローバルに取得できるようにします
angular.kawaz = angular.module('kawaz', ['ngSanitize']).config( ($interpolateProvider) ->
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
)
