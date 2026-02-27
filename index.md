---
layout: default
title: Home
---

<div class="post-feed">
  {% for post in paginator.posts %}
    <a class="post-card" href="{{ post.url | relative_url }}">
      <div class="pc-meta">
        <div class="pc-avatar">{{ post.title | slice: 0, 1 | upcase }}</div>
        {% if post.categories %}
          <span>{{ post.categories | first }}</span>
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

<!-- Pagination -->
{% if paginator.total_pages > 1 %}
<nav class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}" class="pagination-prev">&larr; 이전</a>
  {% endif %}

  <span class="pagination-info">
    {{ paginator.page }} / {{ paginator.total_pages }}
  </span>

  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}" class="pagination-next">다음 &rarr;</a>
  {% endif %}
</nav>
{% endif %}
