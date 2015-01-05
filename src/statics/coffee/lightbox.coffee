$ ->
  $imgs = $('.markdown img')
  $imgs.each((index) ->
    src = $(@).attr('src')
    $existingWrapper = $(@).closest('a[data-lightbox]')
    unless $existingWrapper.size()
      $wrapper = $('<a>').attr('data-lightbox', 'article')
      $wrapper.attr('href', src)
      $(@).wrap($wrapper)
  )
