---
layout: default
title: Home
---

<div class="hero">
  <h1>{{ site.title }}</h1>
  <p>{{ site.description }}</p>
</div>

<div class="category-grid">
  <a href="{{ '/cs_fundamentals/' | relative_url }}" class="category-card">
    <h3>CS Fundamentals</h3>
    <p>Operating Systems, Computer Architecture, Networks, and Logic.</p>
  </a>

  <a href="{{ '/programming/' | relative_url }}" class="category-card">
    <h3>Programming</h3>
    <p>Rust, Python, Systems Language, and development techniques.</p>
  </a>
</div>

<section style="margin-top: 40px;">
  <h2 style="margin-bottom: 24px; font-size: 1.5rem;">Recent Notes</h2>
  <div class="post-list">
    {% for post in site.posts limit:5 %}
    <div style="margin-bottom: 24px;">
      <a href="{{ post.url | relative_url }}" style="font-size: 1.1rem; font-weight: 600; text-decoration: none; color: var(--link);">{{ post.title }}</a>
      <p style="color: var(--text-secondary); font-size: 0.95rem; margin-top: 4px;">{{ post.excerpt | strip_html | truncate: 140 }}</p>
    </div>
    {% endfor %}
  </div>
</section>
