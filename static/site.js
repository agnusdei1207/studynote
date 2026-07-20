const inputs = document.querySelectorAll("[data-filter-input]");

for (const input of inputs) {
  const scope = input.closest("section") ?? document;
  const items = scope.querySelectorAll("[data-filter-item]");

  input.addEventListener("input", () => {
    const query = input.value.trim().toLocaleLowerCase("ko");
    for (const item of items) {
      item.hidden = query.length > 0
        && !item.textContent.toLocaleLowerCase("ko").includes(query);
    }
  });
}
