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
    return '<div class="post-card-wrapper">' +
      '<a class="post-card" href="' + post.url + '">' +
        '<div class="pc-meta">' +
          '<div class="pc-avatar">' + avatar + '</div>' +
          catHtml +
          '<span style="opacity: 0.5;">•</span>' +
          '<span>' + post.date + '</span>' +
        '</div>' +
        '<div class="pc-title">' + post.title + '</div>' +
        '<div class="pc-excerpt">' + post.excerpt + '</div>' +
      '</a>' +
      '<button class="card-copy-btn" data-url="' + post.url + '" title="Copy content">' +
        '<svg class="icon-copy" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
          '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>' +
          '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>' +
        '</svg>' +
        '<svg class="icon-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
          '<polyline points="20 6 9 17 4 12"/>' +
        '</svg>' +
      '</button>' +
    '</div>';
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

  // Copy button handler
  feed.addEventListener('click', function(e) {
    var btn = e.target.closest('.card-copy-btn');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    var url = btn.dataset.url;
    fetch(url)
      .then(function(res) { return res.text(); })
      .then(function(html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var content = doc.querySelector('.post-content');
        if (content) {
          var text = content.innerText || content.textContent;
          navigator.clipboard.writeText(text).then(function() {
            btn.classList.add('copied');
            setTimeout(function() { btn.classList.remove('copied'); }, 2000);
          });
        }
      });
  });
})();
</script>
