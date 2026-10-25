(async () => {
  const yearGroups = await loadJSON("data/books.json");
  const bookList = document.getElementById("books");

  yearGroups.forEach(group => {
    const section = document.createElement("section");
    section.className = "book-year";

    const heading = document.createElement("h2");
    heading.textContent = group.year;

    const books = document.createElement("div");
    books.className = "book-list";

    group.books.forEach(book => {
      const item = document.createElement("article");
      item.className = "book-item";

      const cover = document.createElement("img");
      cover.className = "book-cover";
      cover.src = book.image;
      cover.alt = book.imageAlt;
      cover.loading = "lazy";
      cover.addEventListener("error", () => {
        cover.remove();
        item.classList.add("book-item--no-cover");
      }, { once: true });

      const details = document.createElement("div");
      const title = document.createElement("h3");
      title.className = "book-title";
      title.textContent = book.title;
      if (book.lang) title.lang = book.lang;

      const author = document.createElement("p");
      author.className = "book-author";
      author.textContent = book.author;

      details.append(title, author);

      if (book.details) {
        const extraDetails = document.createElement("p");
        extraDetails.className = "book-publisher";
        extraDetails.textContent = book.details;
        details.appendChild(extraDetails);
      }

      const publisher = document.createElement("p");
      publisher.className = "book-publisher";
      publisher.textContent = book.publisher;
      details.appendChild(publisher);

      if (book.completed) {
        const completed = document.createElement("p");
        completed.className = "book-completed";
        completed.textContent = `Completed ${book.completed}`;
        details.appendChild(completed);
      }

      item.append(cover, details);
      books.appendChild(item);
    });

    section.append(heading, books);
    bookList.appendChild(section);
  });
})();