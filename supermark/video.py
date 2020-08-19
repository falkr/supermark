from pathlib import Path

import pypandoc
import requests

from .chunks import YAMLChunk


def download_preview(url, target_path):
    if not target_path.exists():
        data = requests.get(url).content
        with open(target_path, "wb") as handler:
            handler.write(data)


class Video(YAMLChunk):
    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=["video"],
            optional=["start", "caption", "position"],
        )

    def get_id(self):
        video = self.dictionary["video"]
        return super().create_hash("{}".format(video))

    def to_html(self):
        html = []
        video = self.dictionary["video"]
        url = "https://youtube-nocookie.com/{}".format(video)
        # url = "https://youtu.be/{}".format(video)
        start = ""
        if "start" in self.dictionary:
            start = "?start={}".format(self.dictionary["start"])
            url = url + start
        if "position" in self.dictionary and self.dictionary["position"] == "aside":
            aside_id = self.get_id()
            html.append(
                '<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id)
            )
            html.append(
                '<a href="{}"><img width="{}" src="https://img.youtube.com/vi/{}/sddefault.jpg"></img></a>'.format(
                    url, 240, video
                )
            )
            if "caption" in self.dictionary:
                html_caption = pypandoc.convert_text(
                    self.dictionary["caption"], "html", format="md"
                )
                html.append(html_caption)
            html.append("</aside>")
        else:
            html.append('<div class="figure">')
            width = 560
            height = 315
            html.append(
                '<iframe width="{}" height="{}" src="https://www.youtube-nocookie.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(
                    width, height, video, start
                )
            )
            if "caption" in self.dictionary:
                html.append(
                    '<span name="{}">&nbsp;</span>'.format(self.dictionary["video"])
                )
                html_caption = pypandoc.convert_text(
                    self.dictionary["caption"], "html", format="md"
                )
                html.append(
                    '<aside name="{}"><p>{}</p></aside>'.format(
                        self.dictionary["video"], html_caption
                    )
                )
            html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder):
        s = []
        url = "https://img.youtube.com/vi/{}/sddefault.jpg".format(
            self.dictionary["video"]
        )
        video_url = "https://youtu.be/{}".format(self.dictionary["video"])
        video_id = self.get_id()
        target_path = self.get_dir_cached() / "{}.jpg".format(video_id)
        download_preview(url, target_path)
        # target_path =  Path('../cached/{}.jpg'.format(video_id))
        target_path = target_path.relative_to(builder.output_file.parent)
        s.append("\n")
        s.append("\\begin{video}[h]")
        s.append("\includegraphics[width=\linewidth]{{{}}}".format(target_path))
        if "caption" in self.dictionary:
            caption = pypandoc.convert_text(
                self.dictionary["caption"], "latex", format="md"
            )
            s.append(
                "\caption{"
                + caption.strip()
                + " \\textcolor{SteelBlue}{\\faArrowCircleRight}~"
                + "\\url{{{}}}".format(video_url)
                + "}"
            )
        else:
            s.append("\caption{")
            s.append("\\url{{{}}}".format(video_url) + "}")
        s.append("\end{video}")
        return "\n".join(s)
