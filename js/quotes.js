(async () => {
  const quotes = await loadJSON("data/quotes.json");
  const quoteList = document.getElementById("quotes");

  quotes.forEach(quote => {
    const figure = document.createElement("figure");
    figure.className = "quote-entry";

    const text = document.createElement("p");
    text.className = "quote-text";
    text.textContent = quote.text;
    if (quote.lang) text.lang = quote.lang;

    const citation = document.createElement("figcaption");
    citation.textContent = quote.citation;

    figure.append(text, citation);
    quoteList.appendChild(figure);
  });
})();