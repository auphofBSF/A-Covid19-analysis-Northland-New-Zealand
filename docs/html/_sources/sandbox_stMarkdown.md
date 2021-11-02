---
substitutions:
  key1: "I'm a **substitution**"
  key2: |
    ```{note}
    {{ key1 }}
    ```
  fishy: |
    ```{image} img/fun-fish.png
    :alt: fishy
    :width: 200px
    ```
---

# Test stMarkdown - Substitution

Inline: {{ key1 }}

Block level:

{{ key2 }}