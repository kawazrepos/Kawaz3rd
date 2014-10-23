from django.forms import CharField
from kawaz.core.forms.widgets import MaceEditorWidget

__author__ = 'giginet'

class MarkdownField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MaceEditorWidget
        kwargs['help_text'] = """記述には「Markdown記法」が利用できます。詳しい使い方は「<a href="/helps/markdown/">Kawazでの記事の書き方</a>」をご覧ください"""
        return super().__init__(*args, **kwargs)