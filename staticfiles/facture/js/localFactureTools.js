function toggleDropdown(button) {
  const dropdownMenu = button.nextElementSibling;

  // Close other dropdowns if open
  document.querySelectorAll(".dropdown-menu.show").forEach((menu) => {
    if (menu !== dropdownMenu) {
      menu.classList.remove("show");
    }
  });

  // Toggle the clicked dropdown
  dropdownMenu.classList.toggle("show");
}

// Close the dropdown if clicking outside
document.addEventListener("click", (event) => {
  if (!event.target.closest(".dropdown")) {
    document.querySelectorAll(".dropdown-menu.show").forEach((menu) => {
      menu.classList.remove("show");
    });
  }
});

function updateItem(pk) {
  const updateUrl = `/facture/local/update/${pk}/`; // Construct URL dynamically
  window.location.href = updateUrl; // Redirect to the update view
}

function deleteItem(pk) {
  const deleteUrl = `/facture/local/delete/${pk}/`; // Construct URL dynamically

  if (confirm("Are you sure you want to delete this facture?")) {
    fetch(deleteUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": "{{ csrf_token }}", // Include CSRF token for security
      },
    })
      .then((response) => {
        if (response.ok) {
          alert("Facture deleted successfully!");
          window.location.href = '/facture/local/';
        } else {
          alert("Failed to delete facture.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred.");
      });
  }
}
