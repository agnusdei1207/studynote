---
layout: default
title: Home
---

<div class="post-feed">
  {% assign all_notes = site.html_pages | concat: site.documents | sort: "date" | reverse %}
  {% for doc in all_notes %}
    {% if doc.title and doc.title != "" and doc.url != "/" and doc.layout != "default" and doc.layout != "folder" %}
    <a class="post-card" href="{{ doc.url | relative_url }}">
      <div class="pc-meta">
        <div class="pc-avatar">{{ doc.title | slice: 0, 1 | upcase }}</div>
        {% if doc.collection %}
          <span>{{ doc.collection }}</span>
        {% elsif doc.dir %}
          <span>{{ doc.dir | remove: "/" | split: "/" | last }}</span>
        {% endif %}
        {% if doc.date %}
          <span style="opacity: 0.5;">•</span>
          <span>{{ doc.date | date: "%B %d, %Y" }}</span>
        {% endif %}
      </div>
      <div class="pc-title">{{ doc.title }}</div>
      <div class="pc-excerpt">
        {% if doc.description %}
          {{ doc.description }}
        {% else %}
          {{ doc.content | strip_html | truncate: 140 }}
        {% endif %}
      </div>
    </a>
    {% endif %}
  {% endfor %}
</div>
