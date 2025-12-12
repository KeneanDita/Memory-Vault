// File upload preview
document.addEventListener("DOMContentLoaded", function () {
  // File input change handler
  const fileInput = document.getElementById("file");
  if (fileInput) {
    fileInput.addEventListener("change", function (e) {
      const fileName = e.target.files[0]?.name || "No file chosen";
      const fileSize = e.target.files[0]?.size || 0;

      // Update file info display
      const fileInfo = document.getElementById("fileInfo");
      if (fileInfo) {
        fileInfo.textContent = `${fileName} (${formatFileSize(fileSize)})`;
      }

      // Validate file size (100MB limit)
      const maxSize = 100 * 1024 * 1024; // 100MB
      if (fileSize > maxSize) {
        alert("File size exceeds 100MB limit");
        e.target.value = "";
      }
    });
  }

  // Auto-switch tab based on file type selection
  const fileTypeSelect = document.getElementById("file_type");
  if (fileTypeSelect) {
    fileTypeSelect.addEventListener("change", function () {
      const tabId = this.value + "-tab";
      const tab = document.getElementById(tabId);
      if (tab) {
        new bootstrap.Tab(tab).show();
      }
    });
  }

  // Initialize tooltips
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => new bootstrap.Tooltip(tooltip));
});

// Format file size
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Confirm delete
function confirmDelete(fileType, itemId, itemName) {
  if (
    confirm(`Are you sure you want to delete "${itemName || "this item"}"?`)
  ) {
    fetch(`/delete/${fileType}/${itemId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.ok) {
        window.location.reload();
      }
    });
  }
}

// Search functionality
function searchFiles() {
  const searchTerm = document.getElementById("searchInput").value;
  const currentTab = document
    .querySelector(".nav-tabs .active")
    .getAttribute("data-bs-target")
    .replace("#", "");

  window.location.href = `/browse?tab=${currentTab}&search=${encodeURIComponent(
    searchTerm
  )}`;
}
