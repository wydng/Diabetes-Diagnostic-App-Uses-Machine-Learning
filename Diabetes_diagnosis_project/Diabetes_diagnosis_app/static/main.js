const home = document.querySelector(".h-home")
const about = document.querySelector(".h-about")
const inf = document.querySelector(".h-inf")
const staff = document.querySelector(".h-staff")

const btnAccess = document.querySelector(".btn-access")
btnAccess.addEventListener("click",function(e){
    e.preventDefault()
})

about.addEventListener("click", function(e){
    console.log(1)
    about.classList.add("active")
    home.classList.remove("active")
    inf.classList.remove("active")
    staff.classList.remove("active")
})