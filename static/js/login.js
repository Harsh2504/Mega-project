document.addEventListener("DOMContentLoaded" , () => {

    const loginForm =document.querySelector("#loginform");
    const signupForm =document.querySelector("#signupform");

    document.querySelector("#signuplink").addEventListener("click", e =>{
        e.preventDefault();
        loginForm.classList.add("form--hidden");
        signupForm.classList.remove("form--hidden");
    });


    document.querySelector("#loginlink").addEventListener("click", e =>{
        e.preventDefault();
        loginForm.classList.remove("form--hidden");
        signupForm.classList.add("form--hidden");
    });
});
function logout()
{
    window.location="l.html"  
}
/*function validate()
{
    var username=document.getElementById("email").value;
    var password=document.getElementById("pwd").value;
   
    if(username=="Harsh" || username=="Sahil" || username=="admin"  && password=="sgp123")
    {
        document.getElementById("btn").onclick=function(){window.location.href = 'admin.html';};
       
        
        return false;
    }
    else{
        alert("Invalid Username and password");

    }
}
*/


 /*setTimeout(function() {
    document.querySelector(".loading-screen").style.transform = "translateY(-100%)";
    setTimeout(function() {
      document.getElementById("loginform").classList.add("show");
    },0450);
  }, 4000);*/
  if (!sessionStorage.getItem('loading-screen-shown')) {
    setTimeout(function() {
      document.querySelector(".loading-screen").style.transform = "translateY(-100%)";
      setTimeout(function() {
        document.getElementById("loginform").classList.add("show");
      }, 450);
    }, 4000);
    sessionStorage.setItem('loading-screen-shown', true);
  } else {
    setTimeout(function() {
      document.querySelector(".loading-screen").style.transition = "transform 0s ";
      document.querySelector(".loading-screen").style.transform = "translateY(-100%)";
      setTimeout(function() {
        document.getElementById("loginform").classList.add("show");
      }, 001);
    }, 0001);
  }
  

  function toggleVisibility() {
    const passwordField = document.getElementById("pwd");
    const eyeIcon = document.querySelector(".fa");
    if (passwordField.getAttribute("type") === "password") {
      passwordField.setAttribute("type", "text");
      eyeIcon.classList.remove("fa-eye");
      eyeIcon.classList.add("fa-eye-slash");
    } else {
      passwordField.setAttribute("type", "password");
      eyeIcon.classList.remove("fa-eye-slash");
      eyeIcon.classList.add("fa-eye");
    }
  }


  