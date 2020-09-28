// main navigation responsive button
function nav_links() {
  document.getElementById("nav_links").classList.toggle("show_nav_links");
  document.getElementById("btn_sus").classList.toggle("btn_sus_hover");
}
// work selector button show works type
function dropDownFunc() {
  document.getElementById("myDropdown").classList.toggle("show");
  var element = document.getElementById("selector_btn");
  element.classList.add("dropbtnHover");
}
// work selector change inner text
function selectorBtnText(name) {
  document.getElementById("selector_btn").innerHTML = name;
}
// filter selector button show filter navigation
$(".selector-filter").click(function () {
  if ($(this).hasClass("filterBtnHover")) {
    $(this).removeClass("filterBtnHover");
  } else {
    $(this).addClass("filterBtnHover");
  }
  $(".filterNav").slideToggle(50, "linear", "filter_nav_show");
});
// time selector button show drop down menu
function time_btn() {
  document.getElementById("timeSelectors").classList.toggle("show");
  var element = document.getElementById("time_btn");
  element.classList.add("dropbtnHover");
}
// time selector change inner text
function timeSelBtn(name) {
  document.getElementById("time_btn").innerHTML = name;
}
// if user click other space exept buttons
window.onclick = function (event) {
  if (
    !event.target.matches(".dropbtn") &&
    !event.target.matches(".dropbtn_time")
  ) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
        var element = document.getElementById("selector_btn");
        element.classList.remove("dropbtnHover");
      }
    }
    var dropdownsMe = document.getElementsByClassName("timeSelect-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdownsMe[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
        var element = document.getElementById("time_btn");
        element.classList.remove("dropbtnHover");
      }
    }
  }
};
// work selector button show works type
function selector_btn() {
  document.getElementById("sidebar_ul").classList.toggle("show");
}
// messages animation
setTimeout(function () {
  $("#alert").fadeOut("fast");
}, 5000); // <-- time in milliseconds
// category navigation buttons
// $("#right").click(function () {
//   $(".works-category").animate({
//     scrollLeft: "+=156px",
//   });
//   $("#right").css("right", "+=-160px");
// });

// $("#left").click(function () {
//   $(".works-category").animate({
//     scrollLeft: "-=200px",
//   });
//   $("#right").css("right", "+=160px");
// });
