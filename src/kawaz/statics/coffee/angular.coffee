# Angular Applicationをグローバルに取得できるようにします
angular.kawaz = angular.module('kawaz', []).config( ($interpolateProvider) ->
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
)