console.log("hello, js")
// ====== Form validation
function validateForm() {
    let query = document.getElementById("form-check").value;

    if (query === "") {
    return false;
  }

  // If all validation passes, allow form submission
  return true;
}

//====== Remove company from watchlist
async function removeCompanyFromWatchlist(watchlistName, companyId) {
  const url = `/watchlist/${watchlistName}/company/${companyId}/`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    });

    if (response.ok) {
      console.log("Company removed from watchlist.");
      location.reload(); // Reload the current page
    } else {
      console.error("Error removing company from watchlist.");
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
}

// Get CSRF token from cookies
function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return "";
}
// Event listeners for removing companies from watchlist
document.addEventListener("DOMContentLoaded", function () {
  const removeBtns = document.querySelectorAll(".remove-company-btn");

  removeBtns.forEach((btn) => {
    btn.addEventListener("click", async function () {
      const watchlistName = btn.dataset.watchlistName;
      const companyId = btn.dataset.companyId;
      await removeCompanyFromWatchlist(watchlistName, companyId);
    });
  });
});
// Event listeners for modal
const openModalBtn = document.getElementById("openModalBtn");
const modal = document.getElementById("modal");
const closeBtn = document.querySelector(".close");

openModalBtn.addEventListener("click", () => {
  modal.style.display = "block";
});

closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

// ===== Dark mode toggle

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
themeToggleLightIcon.classList.remove('hidden');
} else {
themeToggleDarkIcon.classList.remove('hidden');
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function() {

// toggle icons inside button
themeToggleDarkIcon.classList.toggle('hidden');
themeToggleLightIcon.classList.toggle('hidden');

// if set via local storage previously
if (localStorage.getItem('color-theme')) {
  if (localStorage.getItem('color-theme') === 'light') {
      document.documentElement.classList.add('dark');
      localStorage.setItem('color-theme', 'dark');
  } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('color-theme', 'light');
  }

// if NOT set via local storage previously
} else {
  if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('color-theme', 'light');
  } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('color-theme', 'dark');
  }
}

});
