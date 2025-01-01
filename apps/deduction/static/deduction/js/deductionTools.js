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
  window.location.href = `/deduction/update/${pk}/`; // Redirect to the update view
}

function deleteItem(pk, typeFacture) {
  const deleteUrl = `/deduction/delete/${pk}/`; // Construct URL dynamically
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
          window.location.href = '/deduction/';
        } else if (response.status === 403) {
          alert("You are not an owner of this deduction!");
          window.location.href = '/deduction/';
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
          window.location.href = '/deduction/';
        } else if (data.error) {
          alert(`Error: ${data.error}`);
        }
      })
      .catch((error) => {
        console.error("Fetch error:", error.message);
      });
  }
}


function toggleDetails(button) {
  const supplierContainer = button.closest(".supplier-container");
  const details = supplierContainer.querySelector(".supplier-details");
  const otherDetails = document.querySelectorAll(".supplier-details");

  // Close all other supplier details
  otherDetails.forEach((detail) => {
    if (detail !== details) {
      detail.style.display = "none";
    }
  });

  // Toggle current supplier details
  if (details.style.display === "none" || details.style.display === "") {
    details.style.display = "block";
    button.textContent = "Hide Details";
  } else {
    details.style.display = "none";
    button.textContent = "Show Details";
  }
}
