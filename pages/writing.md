# Writing Supermark Documents

# Chunks

# Markdown Chunks

The Markdown chunks of the document should follow [Pandoc's Markdown syntax](https://pandoc.org/MANUAL.html#pandocs-markdown).

## Sections

Sections on different levels are written with preceeding `#`, `##`, `###`

```markdown
# Section Level 1
```

```markdown
## Section Level 2
```

```markdown
### Section Level 3
```

## Text Markup

**bold** text __bold__ text.
*emphasized* text, _emphasized text_




## Lists




# YAML Elements

YAML elements start and stop with a delimiter `---`.


## Referenced Chunks

Use a chunk as a reference to other chunks defined in other files.

```yaml
---
ref: file.md
---
```

## Videos


---
type: youtube
video: wupToqz1e2g
caption: "The Pale Blue Dot."
start: 80
---

```yaml
---
type: youtube
video: wupToqz1e2g
position: aside
caption: "The Pale Blue Dot."
start: 80
---
```

## Tables

Tables can be included directly as HTML, or via the following YAML section that refers to a table stored in a file.
The table in the file must use the [mediawiki syntax for tables](https://www.mediawiki.org/wiki/Help:Tables), with an example shown below.
The optional class attribute places a `<div>` element around the table for styling with the given class.

The optional format attribute allows to select the markup within the cells. Examples are html, markdown, wikimedia, latex.

```yaml
---
type: table
file: tables/table.mw
class: rubric
caption: "Table with a caption."
---
```

```mediawiki
{|
|Orange
|Apple
|-
|Bread
|Pie
|-
|Butter
|Ice cream 
|}
```



## Figures

## Buttons

## Hints

Hints are boxes with information that is only visible when the reader clicks on the header.
The top of the hint is specified with a YAML section. 
The content of the hint is provided as post-YAML section, directly following the YAML header.
It ends after two consecutive empty lines.

---
type: hint
title: Hint about Something
---
Within the content you can have lists:

* 10.0.0.0/8
* 172.16.0.0/12
* 192.168.0.0/16

And you can continue.

**Remember:** Hints should be helpful. 


```yaml
---
type: hint
title: Hint about Something
---
Within the content you can have lists:

* 10.0.0.0/8
* 172.16.0.0/12
* 192.168.0.0/16

An you can coninue.

**Remember:** Hints should be helpful. 
```


# HTML Blocks


# Code Blocks

Supermark  uses Pandoc's functions to highlight code. Place the code between the following delimiters:


<div>
<pre>
```bash
pandoc --list-highlight-languages
```
</pre>
</div>


`abc`, `asn1`, `asp`, `ats`, `awk`, `actionscript`, `ada`, `agda`, `alertindent`, `apache`, `bash`, `bibtex`, `boo`, `c`, `cs`, `cpp`, `cmake`, `css`, `changelog`, `clojure`, `coffee`, `coldfusion`, `commonlisp`, `curry`, `d`, `dtd`, `diff`, `djangotemplate`, `dockerfile`, `doxygen`, `doxygenlua`, `eiffel`, `elixir`, `email`, `erlang`, `fsharp`, `fortran`, `gcc`, `glsl`, `gnuassembler`, `m4`, `go`, `html`, `hamlet`, `haskell`, `haxe`, `ini`, `isocpp`, `idris`, `fasm`, `nasm`, `json`, `jsp`, `java`, `javascript`, `javadoc`, `julia`, `kotlin`, `llvm`, `latex`, `lex`, `lilypond`, `literatecurry`, `literatehaskell`, `lua`, `mips`, `makefile`, `markdown`, `mathematica`, `matlab`, `maxima`, `mediawiki`, `metafont`, `modelines`, `modula2`, `modula3`, `monobasic`, `ocaml`, `objectivec`, `objectivecpp`, `octave`, `opencl`, `php`, `povray`, `pascal`, `perl`, `pike`, `postscript`, `powershell`, `prolog`, `pure`, `purebasic`, `python`, `r`, `relaxng`, `relaxngcompact`, `roff`, `ruby`, `rhtml`, `rust`, `sgml`, `sql`, `sqlmysql`, `sqlpostgresql`, `scala`, `scheme`, `tcl`, `tcsh`, `texinfo`, `mandoc`, `vhdl`, `verilog`, `xml`, `xul`, `yaml`, `yacc`, `zsh`, `dot`, `noweb`, `rest`, `sci`, `sed`, `xorg`, `xslt`,

For an updated list, type:

```bash
pandoc --list-highlight-languages
```

# File Encoding

  - UTF-8


# Special

### Learning Goals

```markdown
:goals:
- Learning Goal 1
- Learning Goal 2


```

End the goal environment with two empty lines.


:goals:
- Learning Goal 1
- Learning Goal 2


## Tips

:tip: A tip is shown in a highlighted box.


```
:tip: A tip is shown in a highlighted box.
```


## Warnings

:warning: Use warnings to prevent harm or damage. Draw attention.


```
:warning: Use warnings to prevent harm or damage. Draw attention.
```



## Solution Hints


:hint: This is a hint that is only visible after clicking a button.



:hint: This is another hint that is only visible after clicking a button.



# Numbered Lists

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non imperdiet mauris. Sed rutrum massa at leo fringilla consequat. Duis eget leo vel augue placerat venenatis nec id lectus. Maecenas aliquam ac lectus sit amet dictum. Mauris odio tortor, tincidunt sed pulvinar in, varius in massa. Curabitur fermentum turpis felis, a egestas diam consectetur et. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam lacinia lobortis accumsan. Quisque bibendum molestie metus, eu pharetra ante cursus eget. Fusce lobortis velit et massa sollicitudin, a bibendum elit commodo. Sed at pretium enim. Nunc viverra feugiat eros, sodales molestie dui lobortis eget. Donec sollicitudin dui commodo, imperdiet nibh eget, faucibus ex.

:steps:
1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non imperdiet mauris. Sed rutrum massa at leo fringilla consequat. Duis eget leo vel augue placerat venenatis nec id lectus. Maecenas aliquam ac lectus sit amet dictum. Mauris odio tortor, tincidunt sed pulvinar in, varius in massa. Curabitur fermentum turpis felis, a egestas diam consectetur et. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam lacinia lobortis accumsan. Quisque bibendum molestie metus, eu pharetra ante cursus eget. Fusce lobortis velit et massa sollicitudin, a bibendum elit commodo. Sed at pretium enim. Nunc viverra feugiat eros, sodales molestie dui lobortis eget. Donec sollicitudin dui commodo, imperdiet nibh eget, faucibus ex.
2. Fusce nisi odio, tincidunt sed dui sit amet, porta volutpat mauris. Nam quis leo at sem fermentum efficitur a non magna. Nullam rutrum sem sed massa efficitur posuere. Nullam leo diam, congue in imperdiet non, aliquet sed est. Quisque et nunc in elit hendrerit feugiat. Nulla euismod iaculis dolor et molestie. Sed ut lectus sagittis, ultrices nulla sagittis, sodales enim. Quisque in tortor nec dui accumsan consectetur. Quisque laoreet auctor congue. Etiam malesuada enim eget risus posuere, ut porta est faucibus. Cras rhoncus sem in aliquet suscipit. Etiam cursus pellentesque mauris, ut sagittis tellus consectetur nec.
3. Mauris feugiat, nisi tempor tincidunt eleifend, ante nisi dictum lectus, nec ultricies magna eros ultrices nisl. Morbi laoreet nibh mi, a maximus augue tristique vitae. Aenean at nisl sit amet nisl eleifend feugiat eget quis lacus. Maecenas ac dignissim libero, vel tristique ante. Donec sollicitudin dapibus turpis vitae consequat. Integer dapibus felis a urna vehicula vehicula. Donec eleifend sed nulla non efficitur. Curabitur ut ligula aliquet, pharetra quam at, auctor augue. Aliquam vel commodo ante. Ut blandit lectus sapien, eget imperdiet diam placerat vel. Vestibulum laoreet velit eu ultrices tincidunt. Curabitur in tristique massa.
4. Cras ultrices mauris risus, vel maximus quam volutpat quis. Nulla facilisi. Nullam suscipit euismod auctor. Etiam sollicitudin diam commodo, elementum nisl quis, commodo quam. Proin a nulla tempor, pretium enim et, euismod eros. Sed rhoncus sagittis lectus, sit amet semper tortor tempus eu. Aenean lorem nisl, luctus sit amet ultricies sed, sodales quis ligula. Mauris eleifend sem lacinia ligula cursus egestas. Phasellus ut ex tortor. Aliquam congue imperdiet nibh eu rhoncus. Ut sed sollicitudin turpis, non gravida nulla.
5. Phasellus rutrum sollicitudin vestibulum. Proin pretium turpis non pellentesque rutrum. Fusce vitae congue metus, at dignissim enim. Sed quis varius metus. Curabitur mattis turpis non nisi imperdiet, nec mattis arcu varius. Maecenas et auctor nisi, ut volutpat diam. Nulla facilisi. Pellentesque semper iaculis lectus, et rutrum metus euismod et. Integer nisl eros, fermentum quis vulputate et, tristique in dolor. Nam rhoncus posuere sem, non volutpat lectus sagittis hendrerit. Quisque eget ornare urna. In feugiat eleifend accumsan. Donec in sapien consequat, dictum massa at, sollicitudin mauris.


:steps:
1. This is the first step
2. This is the second step.
3. This is the third step.

