from .chunks import Chunk
import pypandoc

class Code(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)

    def to_html(self):
        extra_args = ['--highlight-style', 'pygments']
        output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
        return output