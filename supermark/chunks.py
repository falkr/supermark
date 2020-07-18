import hashlib
import pypandoc
import yaml
from .parse import RawChunk, ParserState
from .tell import tell

shake = hashlib.shake_128()

class Chunk:
    """ Base class for a chunk.
    """
    def __init__(self, raw_chunk, page_variables):
        self.raw_chunk = raw_chunk
        self.page_variables = page_variables
        self.aside = False
        self.asides = []

    def is_aside(self):
        return self.aside

    def get_asides(self):
        return self.asides

    def get_first_line(self):
        return self.raw_chunk.lines[0]

    def get_type(self):
        return self.raw_chunk.type
    
    def get_start_line_number(self):
        return self.raw_chunk.start_line_number

    def get_content(self):
        return ''.join(self.raw_chunk.lines)
    
    @staticmethod
    def create_hash(content):
        shake.update(content)
        return shake.hexdigest(3)


class YAMLChunk(Chunk):

     def __init__(self, raw_chunk, dictionary, page_variables, required=None, optional=None):
          super().__init__(raw_chunk, page_variables)
          self.dictionary = dictionary
          required = required or []
          optional = optional or []
          for key in required:
               if key not in self.dictionary:
                    tell("YAML section misses required parameter '{}'.".format(key), level='error', chunk=raw_chunk)
          for key in self.dictionary.keys():
               if (key not in required) and (key not in optional) and (key != 'type'):
                    tell("YAML section has unknown parameter '{}'.".format(key), level='warn', chunk=raw_chunk)
                    

class YAMLDataChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, optional=['status'])


class MarkdownChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
        self.content = ''.join(self.raw_chunk.lines)
        self.is_section = super().get_first_line().startswith('# ')
        if raw_chunk.get_tag() is not None:
            self.class_tag = super().get_first_line().strip().split(':')[1].lower()
            self.aside = self.class_tag=='aside'
            self.content = self.content[len(self.class_tag)+2:].strip()
        else:
            self.class_tag = None
            self.aside = False

    def get_content(self):
        return self.content
        
    def pandoc_to_html(self):
        extra_args = ['--ascii', '--highlight-style', 'pygments']
        extra_args = ['--highlight-style', 'pygments']
        return pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
    
    def to_html(self):
        if self.aside:
            shake.update(self.content.encode('utf-8'))
            aside_id = shake.hexdigest(3)
            output = []
            output.append('<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id))
            output.append(self.pandoc_to_html())
            output.append('</aside>')
            return ''.join(output)
        else:
            if self.class_tag:
                output = self.pandoc_to_html()
                output = '<div class="{}">{}</div>'.format(self.class_tag, output)
            else:
                output = self.pandoc_to_html()
            return output


class HTMLChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
    
    def to_html(self):
        return super().get_content()
