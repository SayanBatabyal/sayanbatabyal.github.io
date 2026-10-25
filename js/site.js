// Shared helpers: loads a JSON file and escapes text for HTML.
async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error("Failed to load " + path);
  return res.json();
}
function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
// Build site navigation from the shared JSON link list.
document.addEventListener("DOMContentLoaded", async () => {
  const navs = document.querySelectorAll("nav[data-site-nav]");
  if (!navs.length) return;

  try {
    const items = await loadJSON("data/nav.json");
    const currentPage = location.pathname.split("/").pop() || "index.html";

    navs.forEach(nav => {
      items.forEach(item => {
        const link = document.createElement("a");
        link.href = item.href;
        link.textContent = item.label;
        if (item.href === currentPage) link.setAttribute("aria-current", "page");
        nav.appendChild(link);
      });
    });
  } catch (error) {
    console.error("Unable to load site navigation.", error);
  }
});
