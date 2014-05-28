import os
import hashlib
import factory
from ..models import Material
from kawaz.core.personas.tests.factories import PersonaFactory

class MaterialFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Material

    @factory.post_generation
    def content_file(self, create, extracted):
        # ファイル名を与えられたら勝手にパスを生成します
        # material = MaterialFactory(content_file='icon.png', author__username='kawaztan')
        # material.content_file = attachments/kawaztan/icon.png
        if not extracted:
            extracted = 'icon.png' # default value
        content_path = os.path.join('attachments', self.author.username, extracted)
        self.content_file = content_path
        return content_path
    author = factory.SubFactory(PersonaFactory)
    ip_address = '0.0.0.0'