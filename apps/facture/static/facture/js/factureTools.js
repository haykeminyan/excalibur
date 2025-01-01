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
  const csrfToken = getCSRFToken();

  if (!csrfToken) {
    alert("CSRF token is missing. Please refresh the page and try again.");
    return;
  }
  window.location.href = `/facture/${typeFacture}/update/${pk}/`; // Redirect to the update view
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
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          alert("Facture deleted successfully!");
          window.location.href = `/facture/${typeFacture}`;
        } else if (response.status === 403) {
          alert("You are not an owner of this facture!");
          window.location.href = `/facture/${typeFacture}`;
        }
        // Check if the response is JSON
        const contentType = response.headers.get("Content-Type");
        if (!contentType || !contentType.includes("application/json")) {
          return response.text().then((text) => {
            throw new Error(`Unexpected response format: ${text}`);
          });
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          alert(data.success);
          window.location.href = `/facture/${typeFacture}`;
        } else if (data.error) {
          alert(`Error: ${data.error}`);
        }
      })
      .catch((error) => {
        console.error("Fetch error:", error.message);
      });
  }
}
