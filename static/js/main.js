document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const menuLinks = document.querySelectorAll(".menu-overlay a");

  menuToggle?.addEventListener("click", () => {
    document.body.classList.toggle("menu--open");
  });

  menuLinks.forEach(link => {
    link.addEventListener("click", () => {
      document.body.classList.remove("menu--open");
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.body.classList.remove("menu--open");
    }
  });
});
