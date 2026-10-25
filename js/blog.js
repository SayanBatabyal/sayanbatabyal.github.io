(async () => {
  const posts = await loadJSON("data/blog.json");
  const ul = document.getElementById("posts");
  posts.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `<a href="${esc(p.url)}">${esc(p.title)}</a><span class="date">(${esc(p.date)})</span>`;
    ul.appendChild(li);
  });
})();
