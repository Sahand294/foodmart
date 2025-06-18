document.addEventListener('DOMContentLoaded',function () {
    const nlt = document.getElementById('nlb')
    const nl = document.querySelector('.nav-link-holder')
    nlt.addEventListener('click',function () {
        nl.classList.toggle('active')
    })
})