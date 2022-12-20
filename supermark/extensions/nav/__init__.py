from typing import Any, Dict, Sequence
from pathlib import Path
from ... import YamlExtension, YAMLChunk, RawChunk, Builder, get_icon


class NavExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="nav", chunk_class=Nav)


class Nav(YAMLChunk):
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
            required=[],
            optional=["prev", "next", "up"],
        )

    def _get_icon(self, link: str) -> str:
        if link == "prev":
            return get_icon("arrow-left-short", size="16")
        elif link == "next":
            return get_icon("arrow-right-short", size="16")
        return ""

    def to_html(self, builder: Builder, target_file_path: Path):
        html: Sequence[str] = []
        html.append('<nav class="d-flex justify-content-between">')
        for link in ["prev", "up", "next"]:
            if link in self.dictionary:
                html.append(
                    f'<a type="button" href="{self.dictionary[link][1]}" class="page-link rounded">{self.dictionary[link][0]}'
                )
                html.append(self._get_icon(link))
                html.append("</a>")
            else:
                html.append("<div></div>")
        return "\n".join(html)
