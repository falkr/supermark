import os
import pypandoc
from .chunks import YAMLChunk
from .tell import tell

class Figure(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['source'], optional=['caption', 'link'])
        file_path = os.path.join(os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary['source'])
        if file_path.startswith('http://') or file_path.startswith('https://'):
            if not os.path.exists(file_path):
                tell('Figure file {} does not exist.'.format(file_path), level='warn')

    def to_html(self):
        html = []
        html.append('<div class="figure">')
        if 'caption' in self.dictionary:
            if 'link' in self.dictionary:
                html.append('<a href="{}"><img src="{}" alt="{}" width="100%"/></a>'.format(self.dictionary['link'], self.dictionary['source'], self.dictionary['caption']))
            else:
                html.append('<img src="{}" alt="{}" width="100%"/>'.format(self.dictionary['source'], self.dictionary['caption']))
            html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['source']))
            html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
            html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['source'], html_caption))
        else:
            if 'link' in self.dictionary:
                html.append('<a href="{}"><img src="{}" width="100%"/></a>'.format(self.dictionary['link'], self.dictionary['source']))
            else:
                html.append('<img src="{}" width="100%"/>'.format(self.dictionary['source']))
        html.append('</div>')
        return '\n'.join(html)