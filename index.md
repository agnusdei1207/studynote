---
layout: default
title: Home
---

<div class="post-feed">
  {% for post in site.posts limit: 20 %}
    <a class="post-card" href="{{ post.url | relative_url }}">
      <div class="pc-meta">
        <div class="pc-avatar">{{ post.title | slice: 0, 1 | upcase }}</div>
        {% if post.categories %}
          <span>{{ post.categories }}</span>
        {% endif %}
        {% if post.date %}
          <span style="opacity: 0.5;">•</span>
          <span>{{ post.date | date: "%B %d, %Y" }}</span>
        {% endif %}
      </div>
      <div class="pc-title">{{ post.title }}</div>
      <div class="pc-excerpt">
        {% if post.description %}
          {{ post.description }}
        {% else %}
          {{ post.content | strip_html | truncate: 140 }}
        {% endif %}
      </div>
    </a>
  {% endfor %}
</div>
