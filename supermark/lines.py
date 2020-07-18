from .chunks import YAMLChunk

class Lines(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['lines'])

    def to_html(self):
        html = []
        for _ in range(self.dictionary['lines']):
            html.append('<hr class="lines"/>')
        return '\n'.join(html)
