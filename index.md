---
layout: default
title: Home
---

<section class="recent-posts">
  <p class="recent-label">최근 노트</p>
  <div class="post-feed">
    {% for post in site.posts limit:3 %}
    <div class="post-card-wrapper">
      <a class="post-card" href="{{ post.url | relative_url }}">
        <div class="pc-meta">
          <span class="pc-avatar">{{ post.title | slice: 0 }}</span>
          <span>{{ post.date | date: "%Y.%m.%d" }}</span>
          {% if post.categories.size > 0 %}
          <span style="opacity:0.4">·</span>
          <span>{{ post.categories | first | replace: '-', ' ' }}</span>
          {% endif %}
        </div>
        <div class="pc-title">{{ post.title }}</div>
        {% if post.excerpt %}
        <div class="pc-excerpt">{{ post.excerpt | strip_html | truncate: 100 }}</div>
        {% endif %}
      </a>
    </div>
    {% endfor %}
  </div>
</section>

