# Writing Supermark Documents


A supermark document is a sequence of several snippets of text, code and data, all in the same file.
A snippet can be for instance plain text, text with some markup, a code example, a link to a video.
These snippets are then treated depending on what they represent.

In general, to start a new snippet, separate them **by two or more blank lines**.




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

## Post-YAML Chunk

## Videos



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
The tabek in the file must use the [mediawiki syntax for tables](https://www.mediawiki.org/wiki/Help:Tables), with an example shown below.
The optional class attribute placed a `<div>` element around the table for styling with the given class.


## Referenced Chunks

Use a chunk as a reference to other chunks defined in other files.

```yaml
---
ref: file.md
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

An you can coninue.

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




# File Encoding

  - UTF-8





