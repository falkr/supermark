import os
import re
import pypandoc
from .chunks import YAMLChunk
from .tell import tell

class Table(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['file'], optional=['class', 'caption'])
        
        file_path = os.path.join(os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary['file'])
        print(file_path)
        self.div_class = None if 'class' not in dictionary else dictionary['class']
        if not os.path.exists(file_path):
            tell('Table file {} does not exist.'.format(file_path), level='error')
        else:
            with open(file_path, 'r') as myfile:
                self.table_raw = myfile.read()

    def to_html(self):
        html = []
        extra_args = ['--from', 'mediawiki', '--to', 'html']
        output = pypandoc.convert_text(self.table_raw, 'html', format='md', extra_args=extra_args)
        if self.div_class:
            output = re.sub('(<table)(>)', '\\1 class="{}"\\2'.format(self.div_class), output)
        html.append(output)
        if 'caption' in self.dictionary:
            html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['file']))
            html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
            html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['file'], html_caption))
        return '\n'.join(html)

    def get_scss(self):
        return """section {
                    border:1px solid #e5e5e5;
                    border-width:1px 0;
                    padding:20px 0;
                    margin:0 0 20px;
                  }"""