document.addEventListener("DOMContentLoaded",function () {
    const nav_button = document.getElementById('mobileMenuToggle')
    const nav_links = document.querySelector('.nav-menu')
    nav_button.addEventListener('click',function () {
        nav_links.classList.toggle('active')
    })
})