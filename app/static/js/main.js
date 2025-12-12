// Memory Vault Main JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => new bootstrap.Tooltip(tooltip));

  // Initialize popovers
  const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
  popovers.forEach((popover) => new bootstrap.Popover(popover));

  // Add animation to stat cards on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fade-in");
      }
    });
  }, observerOptions);

  // Observe all cards for animation
  document.querySelectorAll(".card").forEach((card) => {
    observer.observe(card);
  });

  // File upload progress simulation
  window.simulateUploadProgress = function (button) {
    const progressBar = button.parentElement.querySelector(".progress-bar");
    let width = 0;
    const interval = setInterval(() => {
      if (width >= 100) {
        clearInterval(interval);
        button.disabled = false;
        button.innerHTML =
          '<i class="bi bi-check-circle me-2"></i>Upload Complete';
        button.classList.remove("btn-primary");
        button.classList.add("btn-success");
      } else {
        width += 5;
        progressBar.style.width = width + "%";
        progressBar.textContent = width + "%";
      }
    }, 100);
  };

  // Search functionality enhancement
  const searchInput = document.querySelector('input[name="search"]');
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const rows = document.querySelectorAll("tbody tr");

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? "" : "none";
      });
    });
  }

  // Theme switcher (optional)
  const themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const currentTheme =
        document.documentElement.getAttribute("data-bs-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-bs-theme", newTheme);
      localStorage.setItem("theme", newTheme);

      this.innerHTML =
        newTheme === "dark"
          ? '<i class="bi bi-moon"></i>'
          : '<i class="bi bi-sun"></i>';
    });

    // Load saved theme
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-bs-theme", savedTheme);
    themeToggle.innerHTML =
      savedTheme === "dark"
        ? '<i class="bi bi-moon"></i>'
        : '<i class="bi bi-sun"></i>';
  }

  // File download counter
  document.querySelectorAll('a[href*="download"]').forEach((link) => {
    link.addEventListener("click", function () {
      const fileName = this.getAttribute("data-filename") || "unknown";
      console.log(`Download initiated: ${fileName}`);
      // You could send analytics here
    });
  });

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Print page functionality
  window.printPage = function () {
    window.print();
  };

  // Copy to clipboard functionality
  window.copyToClipboard = function (text) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        alert("Copied to clipboard!");
      })
      .catch((err) => {
        console.error("Failed to copy: ", err);
      });
  };

  // Responsive table handling
  function handleResponsiveTables() {
    const tables = document.querySelectorAll(".table-responsive");
    tables.forEach((table) => {
      if (table.offsetWidth < table.scrollWidth) {
        table.parentElement.classList.add("table-scroll-hint");
      }
    });
  }

  handleResponsiveTables();
  window.addEventListener("resize", handleResponsiveTables);

  // Smooth scroll to top
  const scrollToTopBtn = document.getElementById("scrollToTop");
  if (scrollToTopBtn) {
    window.addEventListener("scroll", function () {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.style.display = "block";
      } else {
        scrollToTopBtn.style.display = "none";
      }
    });

    scrollToTopBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Form validation enhancement
  const forms = document.querySelectorAll("form[novalidate]");
  forms.forEach((form) => {
    form.addEventListener(
      "submit",
      function (event) {
        if (!this.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        this.classList.add("was-validated");
      },
      false
    );
  });

  // Initialize
  console.log("Memory Vault UI initialized");
});
