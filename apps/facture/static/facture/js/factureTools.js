// Retrieve CSRF token from meta tag
function getCSRFToken() {
  const tokenMeta = document.querySelector('meta[name="csrf-token"]');
  if (!tokenMeta) {
    console.error("CSRF token not found in meta tags.");
    return null;
  }
  return tokenMeta.getAttribute("content");
}

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

function updateItem(pk, typeFacture) {
  const updateUrl = `/facture/${typeFacture}/update/${pk}/`; // Construct URL dynamically
  window.location.href = updateUrl; // Redirect to the update view
}

function deleteItem(pk, typeFacture) {
  const deleteUrl = `/facture/${typeFacture}/delete/${pk}/`; // Construct URL dynamically
  const csrfToken = getCSRFToken();

  if (!csrfToken) {
    alert("CSRF token is missing. Please refresh the page and try again.");
    return;
  }

  if (confirm("Are you sure you want to delete this facture?")) {
    fetch(deleteUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken, // Include CSRF token dynamically
        "Content-Type": "application/json", // Ensure content type is correct
      },
    })
      .then((response) => {
        if (response.ok) {
          alert("Deduction deleted successfully!");
          window.location.href = `/facture/${typeFacture}`;
        } else {
          response.text().then((text) => {
            console.error("Server error response:", text);
            alert("Failed to delete deduction. Please try again.");
          });
        }
      })
      .catch((error) => {
        console.error("Network error:", error);
        alert("An error occurred. Please check your connection and try again.");
      });
  }
}
