sticky = 0;

window.onload = function () {
    
    let navbar = document.getElementById("navbar");
   sticky = navbar.offsetTop;
    window.onscroll = function () { myFunction() };
}

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}
