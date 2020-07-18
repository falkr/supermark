from .chunks import YAMLChunk
import pypandoc

class Video(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['video'], optional=['start', 'caption', 'position'])
    
    def to_html(self):
        html = []
        video = self.dictionary['video']
        url = 'https://youtu.be/{}'.format(video)
        start = ''
        if 'start' in self.dictionary:
            start = '?start={}'.format(self.dictionary['start'])
            url = url + start
        if 'position' in self.dictionary and self.dictionary['position']=='aside':
            aside_id = super().create_hash('{}'.format(video).encode('utf-8'))
            html.append('<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id))
            html.append('<a href="{}"><img width="{}" src="https://img.youtube.com/vi/{}/sddefault.jpg"></img></a>'.format(url, 240, video))
            if 'caption' in self.dictionary:
                html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
                html.append(html_caption)
            html.append('</aside>')
        else:
            html.append('<div class="figure">')
            width = 560
            height = 315
            html.append('<iframe width="{}" height="{}" src="https://www.youtube.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(width, height, video, start))
            if 'caption' in self.dictionary:
                html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['video']))
                html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
                html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['video'], html_caption))
            html.append('</div>')
        return '\n'.join(html)