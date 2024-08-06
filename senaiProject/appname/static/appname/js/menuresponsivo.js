const body = document.querySelector("body"),
      nav = document.querySelector("nav"),
      modeToggle = document.querySelector(".cart"),
      sidebarOpen = document.querySelector(".sidebarOpen"),
      sidebarClose = document.querySelector(".sidebarClose");

// Toggle sidebar
sidebarOpen.addEventListener("click", () => {
    nav.classList.add("active");
});

sidebarClose.addEventListener("click", () => {
    nav.classList.remove("active");
});

body.addEventListener("click", (e) => {
    let clickedElm = e.target;
    if (!clickedElm.classList.contains("sidebarOpen") && !clickedElm.closest(".menu")) {
        nav.classList.remove("active");
    }
});

