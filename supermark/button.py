from .chunks import YAMLChunk

class Button(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['url', 'text'])

    def to_html(self):
        clazz = 'ntnu-button'
        html = []
        html.append('<a class="{}" href="{}">{}</a>'.format(clazz, self.dictionary['url'], self.dictionary['text']))
        return '\n'.join(html)