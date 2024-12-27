document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.getElementById("filter_option");
  const searchInput = document.getElementById("search");
  const addFilterButton = document.getElementById("add-filter-btn");
  const form = document.querySelector(".search-form");

  // Update search input name based on dropdown value
  const updateSearchInputName = (input, value) => {
    input.name = value || "";
    input.value = ""; // Clear the input box
  };

  // Handle initial dropdown change for the main filter
  if (dropdown && searchInput) {
    dropdown.addEventListener("change", () => {
      updateSearchInputName(searchInput, dropdown.value);
    });
    updateSearchInputName(searchInput, dropdown.value); // Initialize search input name
  }

  // Add a new filter block with dropdown and search input
  const createFilterBlock = () => {
    const filterContainer = document.createElement("div");
    filterContainer.classList.add("filter-container");

    // Create dropdown
    const newDropdown = document.createElement("select");
    newDropdown.classList.add("filter-dropdown");

    // Add options to dropdown
    const options = [
      { value: "", text: "--Select Filter--" },
      { value: "number_facture", text: "Number facture" },
      { value: "date", text: "Created date" },
      { value: "reference", text: "Reference" },
      { value: "quantity", text: "Quantity" },
      { value: "percent", text: "Percent" },
      { value: "total_tax", text: "Total Tax" },
      { value: "total_payment_after_tax", text: "Total payment after tax" },
    ];

    options.forEach(({ value, text }) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = text;
      newDropdown.appendChild(option);
    });

    // Create search input
    const newSearchInput = document.createElement("input");
    newSearchInput.type = "text";
    newSearchInput.classList.add("search-box");
    newSearchInput.placeholder = "Search...";
    updateSearchInputName(newSearchInput, ""); // Initialize with an empty name

    // Update search input name on dropdown change
    newDropdown.addEventListener("change", () => {
      updateSearchInputName(newSearchInput, newDropdown.value);
    });

    // Append dropdown and input to the filter container
    filterContainer.appendChild(newDropdown);
    filterContainer.appendChild(newSearchInput);

    // Add the filter container to the form
    form.insertBefore(filterContainer, addFilterButton);
  };

  // Add event listener to the "Add Filter" button
  if (addFilterButton && form) {
    addFilterButton.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent form submission
      createFilterBlock();
    });
  }

  // Add event listener for Clear Filters button
  const clearFiltersButton = document.getElementById("clear-filters-btn");

  if (clearFiltersButton) {
    clearFiltersButton.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent form submission
      const form = document.querySelector(".search-form");
      if (form) {
        form.reset(); // Reset all form inputs
      }
      // Reload the page without query parameters
      window.location.href = window.location.pathname;
    });
  }
});
