$ ->
  # ログインユーザーはMace Editorを使える
  $('.comment-form.authenticated-form').find('#id_comment').addClass('mace-editor')
