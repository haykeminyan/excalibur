document.addEventListener("DOMContentLoaded", () => {
  const clearFiltersButton = document.getElementById("clear-filters-btn");
  const form = document.querySelector(".search-form");

  // Add event listener for Clear Filters button
  if (clearFiltersButton) {
    clearFiltersButton.addEventListener("click", () => {
      if (form) {
        form.reset(); // Reset the search field
      }
      // Reload the page without query parameters
      window.location.href = window.location.pathname;
    });
  }
});
