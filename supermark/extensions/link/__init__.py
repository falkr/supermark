from typing import Any, Dict, Sequence
from pathlib import Path
from ... import YamlExtension, YAMLChunk, RawChunk, Builder, get_icon


class LinkExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="link", chunk_class=Link)


class Link(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=["link", "title"],
            optional=["text", "icon"],
        )

    def to_html(self, builder: Builder, target_file_path: Path):
        html: Sequence[str] = []
        html.append('<div class="card mt-3">')
        html.append('<div class="card-body">')
        html.append(f'<a href="{self.dictionary["link"]}" class="stretched-link">')
        if "icon" in self.dictionary:
            html.append(get_icon(self.dictionary["icon"], size="16"))
        html.append(f'<span class="ms-3">{self.dictionary["title"]}</span>')
        if "text" in self.dictionary:
            html.append(
                f'<span class="text-muted ms-3">{self.dictionary["text"]}</span>'
            )
        html.append("</a>")
        html.append("</div>")
        html.append("</div>")
        return "\n".join(html)
