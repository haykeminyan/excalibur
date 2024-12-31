        // Retrieve CSRF token from meta tag
function getCSRFToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    if (!tokenMeta) {
        console.error("CSRF token not found in meta tags.");
        return null;
    }
    return tokenMeta.getAttribute('content');
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

        function updateItem(pk) {
            const updateUrl = `/deduction/update/${pk}/`; // Construct URL dynamically
            window.location.href = updateUrl; // Redirect to the update view
        }

function deleteItem(pk) {
    const deleteUrl = `/deduction/delete/${pk}/`; // Construct URL dynamically
    const csrfToken = getCSRFToken();

    if (!csrfToken) {
        alert("CSRF token is missing. Please refresh the page and try again.");
        return;
    }

    if (confirm("Are you sure you want to delete this deduction?")) {
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
                window.location.href = "/deduction/";
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

        function toggleDetails(button) {
            const supplierContainer = button.closest('.supplier-container');
            const details = supplierContainer.querySelector('.supplier-details');
            const otherDetails = document.querySelectorAll('.supplier-details');

            // Close all other supplier details
            otherDetails.forEach(detail => {
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