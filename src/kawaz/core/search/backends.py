from haystack.backends.elasticsearch_backend import (
    ElasticsearchSearchBackend,
    ElasticsearchSearchEngine,
)

class KuromojiElasticBackend(ElasticsearchSearchBackend):

    DEFAULT_ANALYZER = "kuromoji_analyzer"

    def __init__(self, connection_alias, **connection_options):
        super(KuromojiElasticBackend, self).__init__(
                                connection_alias, **connection_options)
        SETTINGS = {
            'settings': {
                "analysis": {
                    "analyzer": {
                        "kuromoji_analyzer" : {
                            "type" : "custom",
                            "tokenizer" : "kuromoji_tokenizer"
                        },
                    },
                    "tokenizer": {
                        "kuromoji" : {
                           "type":"kuromoji_tokenizer"
                        },
                    },
                    "filter": {
                        "kuromoji_rf":{
                            "type":"kuromoji_readingform",
                            "use_romaji" : "true"
                        },
                        "kuromoji_pos" : {
                            "type": "kuromoji_part_of_speech",
                            "enable_position_increment" : "false",
                            "stoptags" : ["# verb-main:", "動詞-自立"]
                        },
                        "kuromoji_ks" : {
                            "type": "kuromoji_stemmer",
                            "minimum_length" : 6
                        },
                    }
                }
            }
        }
        setattr(self, 'DEFAULT_SETTINGS', SETTINGS)

    def build_schema(self, fields):
        # http://www.wellfireinteractive.com/blog/custom-haystack-elasticsearch-backend/
        # https://github.com/voluntas/downpour/blob/develop/downpour/haystack/backends/elasticsearch_backend.py
        content_field_name, mapping = super(KuromojiElasticBackend,
                                              self).build_schema(fields)

        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]

            if field_mapping['type'] == 'string' and field_class.indexed:
                if not hasattr(field_class, 'facet_for') and not \
                                  field_class.field_type in('ngram', 'edge_ngram'):
                    field_mapping['analyzer'] = self.DEFAULT_ANALYZER
            mapping.update({field_class.index_fieldname: field_mapping})
        return (content_field_name, mapping)


class KuromojiElasticsearchSearchEngine(ElasticsearchSearchEngine):
    backend = KuromojiElasticBackend
