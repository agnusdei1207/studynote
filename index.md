---
layout: default
title: Home
---

<div class="post-feed">
  {% assign all_notes = site.html_pages | concat: site.documents | sort: "date" | reverse %}
  {% for doc in all_notes %}
    {% unless doc.url == '/' or doc.title == nil or doc.title == '' or doc.layout == 'default' or doc.layout == 'folder' %}
    <a class="post-card" href="{{ doc.url | relative_url }}">
      <div class="pc-meta">
        <div class="pc-avatar">{{ doc.title | slice: 0, 2 | upcase }}</div>
        {% if doc.date %}
        <span class="pc-date">{{ doc.date | date: "%Y.%m.%d" }}</span>
        {% endif %}
        {% if doc.collection %}
        <span class="pc-category">{{ doc.collection }}</span>
        {% elsif doc.dir %}
        <span class="pc-category">{{ doc.dir | remove: "/" | split: "/" | last }}</span>
        {% endif %}
      </div>
      <div class="pc-title">{{ doc.title }}</div>
      <div class="pc-excerpt">{{ doc.content | strip_html | normalize_whitespace | truncate: 160 }}</div>
    </a>
    {% endunless %}
  {% endfor %}
</div>
