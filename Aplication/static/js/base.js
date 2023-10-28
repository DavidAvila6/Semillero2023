const menuToggle = document.querySelector(".menu-toggle");
    const navbarMenu = document.querySelector(".navbar-menu");
    
    menuToggle.addEventListener("click", () => {
        navbarMenu.classList.toggle("show-menu");
    });
