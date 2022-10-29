from ... import YamlExtension, YAMLChunk, RawChunk, Builder, Chunk
from typing import Dict, Any, List, Sequence, Optional


class CardExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="card", chunk_class=Card)


class CardGroupExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="cards", chunk_class=CardGroup)


class CardGroup(YAMLChunk):
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
            required=None,
            optional=["columns"],
        )
        self.chunks: List[Chunk] = []

    def accepts(self, chunk: Chunk) -> bool:
        return isinstance(chunk, Card)

    def is_group(self) -> bool:
        return True

    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    def finish(self):
        ...

    def to_html(self, builder: Builder) -> Optional[str]:
        html: Sequence[str] = []
        columns = self.dictionary["columns"] if "columns" in self.dictionary else 2

        if columns < 1 or columns > 3:
            self.warning("Columsn set to two")
            columns = 2

        html.append(f'<div class="row row-cols-1 row-cols-md-{columns} g-4 mb-5">')
        for chunk in self.chunks:
            c = chunk.to_html(builder=builder)
            if c:
                html.append('<div class="col">')
                html.append(c)
                html.append("</div>")
        html.append("</div>")
        return "\n".join(html)


class Card(YAMLChunk):
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
            required=None,
            optional=[
                "link",
                "title",
                "kind",
                "name",
                "detail",
                "image",
                "email",
                "text",
                "link_title",
            ],
        )

    def is_groupable(self) -> bool:
        return True

    def get_group(self) -> Any:
        return CardGroup(self.raw_chunk, {"type": "cards"}, self.page_variables)

    def _create_card_person(
        self, name: str, email: str, detail: str, img: str, html: List[str]
    ):
        html.append(
            '<div class="card mb-3 border-0 person-card" style="max-width: 540px;">'
        )
        html.append('    <div class="row g-0">')
        html.append('        <div class="col-md-2">')
        html.append(
            f'            <img src="{img}" class="img-fluid" alt="Photo of {name}">'
        )
        html.append("        </div>")
        html.append('        <div class="col-md-10">')
        html.append(
            '            <div class="card-body" style="padding: 0px 0px 0px 5px">'
        )
        html.append(f'                <div class="person-card-name">{name}</div>')
        html.append(f'                <div class="person-card-detail">{detail}</div>')
        html.append(
            f'                <a class="person-card-email stretched-link" href="mailto:{email}">{email}</a>'
        )
        html.append("            </div>")
        html.append("        </div>")
        html.append("        </div>")
        html.append("</div>")

    def _create_card_arrow(self, title: str, href: str, html: List[str]):
        html.append('<div class="card text-end shadow-sm">')
        html.append('<div class="card-body">')
        html.append(f'    <h5 class="card-title">{title}</h5>')
        html.append(f'    <a href="{href}" class="stretched-link">')
        html.append('    <i class="bi bi-arrow-right-circle fs-1"></i>')
        html.append("    </a>")
        html.append("</div>")
        html.append("</div>")

    def _create_card_text(
        self,
        title: str,
        text: str,
        link: str,
        html: List[str],
        link_title: Optional[str] = None,
    ):
        html.append('    <div class="card shadow-sm">')
        html.append('    <div class="card-body">')
        html.append(f'        <h5 class="card-title">{title}</h5>')
        html.append(f'        <p class="card-text">{text}</p>')
        if link_title is None:
            html.append(f'        <a href="{link}" class="stretched-link"></a>')
        else:
            html.append("<ul>")
            html.append(
                f'    <li><a href="{link}" class="stretched-link">{link_title}</a></li>'
            )
            html.append("</ul>")
        html.append("    </div>")
        html.append("    </div>")

    def to_html(self, builder: Builder):
        html: Sequence[str] = []

        link = self.dictionary["link"] if "link" in self.dictionary else ""
        link_title = (
            self.dictionary["link_title"] if "link_title" in self.dictionary else None
        )
        type = self.dictionary["type"]
        name = self.dictionary["name"] if "name" in self.dictionary else ""
        email = self.dictionary["email"] if "email" in self.dictionary else ""
        detail = self.dictionary["detail"] if "detail" in self.dictionary else ""
        title = self.dictionary["title"] if "title" in self.dictionary else ""
        image = self.dictionary["image"] if "image" in self.dictionary else ""
        text = self.dictionary["text"] if "text" in self.dictionary else ""

        if type == "card/person":
            self._create_card_person(name, email, detail, image, html)
        elif type == "card/arrow":
            self._create_card_arrow(title, link, html)
        elif type == "card/text":
            self._create_card_text(title, text, link, html, link_title)

        return "\n".join(html)
