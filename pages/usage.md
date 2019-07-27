# Usage


## Default Directory Structure

- course/
    - pages/
        - index.md
        - hello.md
    - templates/
        - page.html
    - assets/
        - ...
    - figures/
        - ...
    - index.html
    - hello.html

## Default Command

Move into the main folder of your project, and invoke the following command:

```
cd course
supermark
````

Supermark will look for *.md files in the pages folder and transform each of them into a html placed at the toplevel.