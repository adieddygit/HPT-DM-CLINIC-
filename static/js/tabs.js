window.onload=function() {

    // get tab container
        var container = document.getElementById("tabContainer");
  
          var tabcon = document.getElementById("tabscontent");
  
          //alert(tabcon.childNodes.item(1));
      // set current tab
      var navitem = document.getElementById("tabHeader_1");
  
  
      //store which tab we are on
      var ident = navitem.id.split("_")[1];
          //alert(ident);
      navitem.parentNode.setAttribute("data-current",ident);
      //set current tab with class of activetabheader
      navitem.setAttribute("class","tabActiveHeader");
  
     // hide two tab contents we don't need
         var pages = tabcon.getElementsByTagName("nav");
          for (var i = 1; i < pages.length; i++) {
            pages.item(i).style.display="none";
          };
  
      //this adds click event to tabs
      var tabs = container.getElementsByTagName("li");
      for (var i = 0; i < tabs.length; i++) {
        tabs[i].onclick=displayPage;
      }
  }
  
  // on click of one of tabs
  function displayPage() {
    var current = this.parentNode.getAttribute("data-current");
    //remove class of activetabheader and hide old contents
    document.getElementById("tabHeader_" + current).removeAttribute("class");
    document.getElementById("tabpage_" + current).style.display="none";
  
    var ident = this.id.split("_")[1];
    //add class of activetabheader to new active tab and show contents
    this.setAttribute("class","tabActiveHeader");
    document.getElementById("tabpage_" + ident).style.display="block";
    this.parentNode.setAttribute("data-current",ident);
  }
  

  document.getElementById('add-more').addEventListener('click', function() {
    // Create a new input group div
    var inputGroup = document.createElement('div');
    inputGroup.className = 'input-group';

    // Create a new input element
    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'lab_investigation_type[]';  // This keeps the input fields as an array in form submission
    newInput.name = 'lab_investigation_result[]';
    newInput.name = 'radiograph_investigation_type[]';
    newInput.name = 'radiograph_investigation_result[]';
    newInput.placeholder = 'Enter Investigation';
    newInput.placeholder = 'Enter Result';
    newInput.required = true;

    // Append the input to the new div
    inputGroup.appendChild(newInput);

    // Append the input group to the form
    document.getElementById('dynamic-form').appendChild(inputGroup);
});

// Toggle the Side Navigation
function toggleNav() {
  const sidenav = document.getElementById("mySidenav");
  const mainContent = document.querySelector(".main-content");
  
  if (sidenav.style.width === "220px") {
      sidenav.style.width = "0";
      mainContent.classList.remove("sidenav-open");
  } else {
      sidenav.style.width = "220px";
      mainContent.classList.add("sidenav-open");
  }
}
