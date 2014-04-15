from django.forms.fields import ImageField

class ImageFormField(ImageField):
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(ImageFormField, self).clean(data, initial)
        else:
            return '__deleted__'
