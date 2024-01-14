function openNav() {
    document.getElementById("sideNav").style.width = "250px";
  }
  
function closeNav() {
    document.getElementById("sideNav").style.width = "0";
  }

var tablinks = document.getElementsByClassName("tab-ls");
var tabcontents = document.getElementsByClassName("tab-con");

function opentab(tabname){
  for(tb of tablinks){
    tb.classList.remove("active-l");
  }
  for(tc of tabcontents){
    tc.classList.remove("active-t");
  }
  event.currentTarget.classList.add("active-l");
  document.getElementById(tabname).classList.add("active-t")
}

