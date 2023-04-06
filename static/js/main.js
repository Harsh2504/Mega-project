function openNav() {
  if (window.innerWidth < 540) {
    var width = "450px";
    var mwid ="0"
  } else {
    var width = "250px";
    var mwid ="250px"
  }
  
  document.getElementById("mySidenav").style.width = width;
  document.getElementById("main").style.marginLeft = mwid;
  
  toggle = !toggle;
  span.innerHTML = "&#10006";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
  toggle = !toggle;
  span.innerHTML = "&#9776";
}

const body3 = document.querySelector('body');
const span = document.getElementById("ham");
let toggle = true;

span.addEventListener("click", function() {
  if (toggle) {
    openNav();
    showSidenav();
  } else {
    closeNav();
    hideSidenav();
  }
});

body3.addEventListener("click", function(event) {
  if (!event.target.closest('#mySidenav') && !event.target.closest('#ham')) {
    closeNav();
    hideSidenav();
    toggle = true;
  }
});


  
const prof = document.getElementById("imageId");
const body2 = document.querySelector("body");
const profdrop = document.getElementById("ulId");
let tog = true;

prof.addEventListener("click", function() {
  if (tog) {
    profdrop.style.visibility = "visible";
    profdrop.style.opacity = 1;
    profdrop.style.display = "flex";
  } else {
    profdrop.style.visibility = "hidden";
    profdrop.style.opacity = 0;
    profdrop.style.display = "none";
  }
  tog = !tog;
});



body2.addEventListener("click", function(event) {
  if (event.target !== prof && !profdrop.contains(event.target)) {
    profdrop.style.visibility = "hidden";
    profdrop.style.opacity = 0;
    profdrop.style.display = "none";
    tog = true;
  }
});
//darkmode 1
 /* const body = document.querySelector('body'), modeSwitch = body.querySelector(".toggle"),   modeText = body.querySelector(".mode-text") ,  lordIcon = body.querySelector("lord-icon");
modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark");
  if (body.classList.contains("dark")) {
    modeText.innerText = "Light mode";
    lordIcon.colors = "outline:#ffffff,primary:#545454,secondary:#8930e8";
    lordIcon.state = "hover-looking-around";
    lordIcon.style = "width:50px;height:50px";
  } else {
    modeText.innerText = "Dark mode";
    lordIcon.colors = "outline:#121331,primary:#ffc738,secondary:#4bb3fd";
    lordIcon.state = "";
    lordIcon.style = "width:50px;height:50px";
  }
});*/
//darkmode 2
const body = document.querySelector('body');
const modeSwitch = body.querySelector('.toggle input');
const modeText = body.querySelector('.mode-text');
const lordIcon = body.querySelector('lord-icon');


// Check if dark mode is stored in local storage
const isDarkMode = localStorage.getItem('darkMode') === 'true';

// Set the initial mode based on local storage value
if (isDarkMode) {
  body.classList.add('dark');
  modeText.innerText = 'Light mode';
  lordIcon.colors = 'outline:#ffffff,primary:#545454,secondary:#8930e8';
  lordIcon.state = 'hover-looking-around';
  lordIcon.style = 'width:50px;height:50px';
} else {
  modeText.innerText = 'Dark mode';
  lordIcon.colors = 'outline:#121331,primary:#ffc738,secondary:#4bb3fd';
  lordIcon.state = '';
  lordIcon.style = 'width:50px;height:50px';
}

// Check if toggle switch is stored in local storage
const isToggleChecked = localStorage.getItem('toggleChecked') === 'true';
if (isToggleChecked) {
  modeSwitch.checked = true;
}

// Listen for clicks on the mode switch
modeSwitch.addEventListener('click', () => {
  // Toggle the "dark" class on the body
  body.classList.toggle('dark');

  // Update the text and icon colors based on the mode
  if (body.classList.contains('dark')) {
    modeText.innerText = 'Light mode';
    lordIcon.colors = 'outline:#ffffff,primary:#545454,secondary:#8930e8';
    lordIcon.state = 'hover-looking-around';
    lordIcon.style = 'width:50px;height:50px';

    // Store the user's preference in local storage
    localStorage.setItem('darkMode', 'true');
  } else {
    modeText.innerText = 'Dark mode';
    lordIcon.colors = 'outline:#121331,primary:#ffc738,secondary:#4bb3fd';
    lordIcon.state = '';
    lordIcon.style = 'width:50px;height:50px';

    // Store the user's preference in local storage
    localStorage.setItem('darkMode', 'false');
  }

  // Store the checked state of the toggle switch in local storage
  localStorage.setItem('toggleChecked', modeSwitch.checked);
});






const sidenav = document.querySelector("#mySidenav");
const links = sidenav.querySelectorAll("a");

for (let i = 0; i < links.length; i++) {
  links[i].style.opacity = 0;
  links[i].style.transform = "translateX(-100%)";
}

  function showSidenav()
{
    for (let i = 0; i < links.length; i++) {
    links[i].style.transition = `0.5s ease-out ${i * 0.1}s`;
    links[i].style.opacity = 1;
    links[i].style.transform = "translateX(0)";
    
  }    }
function hideSidenav() {
  for (let i = 0; i < links.length; i++) {
    links[i].style.opacity = 0;
    links[i].style.transform = "translateX(-100%)";
    links[i].style.transition = "";
  }


}

function tran(){
  for (let i = 0; i < links.length; i++) {
    links[i].style.transition = `0.2s ease-out `;

    
  }  
}


const addButton = document.getElementById("addButton");
const formContainer = document.getElementById("formContainer");

addButton.addEventListener("click", function() {
  if (formContainer.style.display === "none") {
    formContainer.style.display = "block";
    formContainer.classList.add("slide-in");
    formContainer.classList.remove("fade-out");
    addButton.innerText = "Close";
  } else {
    formContainer.classList.remove("slide-in");
    formContainer.classList.add("fade-out");
    addButton.innerText = "Add";
    setTimeout(() => {
      formContainer.style.display = "none";
    }, 500);
  }
});



