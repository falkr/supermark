from .chunks import Chunk, MarkdownChunk

HINT = []
HINT.append('</section>')
HINT.append('<section class="content">')
HINT.append('<div class="hint_title">{}')
HINT.append('<button type="button" class="btn btn-dark btn-sm" style="float: right" onclick="document.getElementById(\'{}\').style.cssText = \'\'">Show</button>')
HINT.append('</div>')
HINT.append('<div class="hint" style="-webkit-filter: blur(5px);" id="{}">{}')
HINT.append('</div>')
HINT.append('</section>')
HINT.append('<section class="content">')
HINT = '\n'.join(HINT)

# the old defunkt hint with a modal dialog
HINT2 = []
HINT2.append('</section>')
HINT2.append('<section class="content">')
HINT2.append('<div class="hint_title">{}')
HINT2.append('<button type="button" class="btn btn-dark btn-sm" style="float: right" data-toggle="modal" data-target="#{}Modal">Show</button>')
HINT2.append('</div>')
HINT2.append('<div class="hint" style="-webkit-filter: blur(5px);" id="{}">{}')
HINT2.append('</div>')
HINT2.append('<div class="modal fade" id="{}Modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">')
HINT2.append('  <div class="modal-dialog" role="document">')
HINT2.append('    <div class="modal-content">')
HINT2.append('      <div class="modal-header">')
HINT2.append('        <h5 class="modal-title" id="exampleModalLabel">Hint</h5>')
HINT2.append('        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
HINT2.append('          <span aria-hidden="true">&times;</span>')
HINT2.append('        </button>')
HINT2.append('      </div>')
HINT2.append('      <div class="modal-body">Are you sure you want to see the hint, or try a bit more on your own?</div>')
HINT2.append('      <div class="modal-footer">')
HINT2.append('        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>')
HINT2.append('        <button type="button" class="btn btn-primary" data-dismiss="modal" onclick="document.getElementById(\'{}\').style.cssText = \'\'">Yes, show me!</button>')
HINT2.append('      </div>')
HINT2.append('    </div>')
HINT2.append('  </div>')
HINT2.append('</div>')
HINT2.append('</section>')
HINT2.append('<section class="content">')
HINT2 = '\n'.join(HINT2)


class Hint(MarkdownChunk):

    def to_html(self):
        output = super().pandoc_to_html()
        title = "Hint"
        body = output
        element_id = Chunk.create_hash(self.content.encode('utf-8'))
        output = HINT.format(title, element_id, element_id, body, element_id, element_id)
        return output