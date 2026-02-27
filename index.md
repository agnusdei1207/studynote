---
layout: default
title: Home
---

<script type="application/json" id="posts-data">
[
{% for post in site.posts %}
{
  "title": {{ post.title | jsonify }},
  "url": {{ post.url | relative_url | jsonify }},
  "categories": {{ post.categories | jsonify }},
  "date": {{ post.date | date: "%B %d, %Y" | jsonify }},
  "excerpt": {{ post.content | strip_html | truncate: 140 | jsonify }}
}{% unless forloop.last %},{% endunless %}
{% endfor %}
]
</script>

<div class="post-feed" id="post-feed">
  <!-- Posts rendered by JS -->
</div>

<div id="load-more-sentinel" style="height: 1px;"></div>

<nav class="pagination" id="pagination" style="display: none;">
  <button id="load-more-btn" class="pagination-next">더 불러오기</button>
</nav>

<script>
(function() {
  var POSTS_PER_PAGE = 20;
  var posts = JSON.parse(document.getElementById('posts-data').textContent || '[]');
  var feed = document.getElementById('post-feed');
  var sentinel = document.getElementById('load-more-sentinel');
  var pagination = document.getElementById('pagination');
  var loadMoreBtn = document.getElementById('load-more-btn');
  var currentIndex = 0;

  function renderPost(post) {
    var avatar = post.title.charAt(0).toUpperCase();
    var catHtml = post.categories ? '<span>' + post.categories + '</span>' : '';
    return '<a class="post-card" href="' + post.url + '">' +
      '<div class="pc-meta">' +
        '<div class="pc-avatar">' + avatar + '</div>' +
        catHtml +
        '<span style="opacity: 0.5;">•</span>' +
        '<span>' + post.date + '</span>' +
      '</div>' +
      '<div class="pc-title">' + post.title + '</div>' +
      '<div class="pc-excerpt">' + post.excerpt + '</div>' +
    '</a>';
  }

  function loadMore() {
    var end = Math.min(currentIndex + POSTS_PER_PAGE, posts.length);
    for (var i = currentIndex; i < end; i++) {
      feed.insertAdjacentHTML('beforeend', renderPost(posts[i]));
    }
    currentIndex = end;

    if (currentIndex >= posts.length) {
      pagination.style.display = 'none';
      sentinel.style.display = 'none';
    } else {
      pagination.style.display = 'flex';
    }
  }

  // Initial load
  loadMore();

  // Intersection Observer for infinite scroll
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting && currentIndex < posts.length) {
        loadMore();
      }
    }, { rootMargin: '200px' });
    observer.observe(sentinel);
    loadMoreBtn.style.display = 'none';
  } else {
    // Fallback: show load more button
    loadMoreBtn.onclick = loadMore;
  }
})();
</script>
