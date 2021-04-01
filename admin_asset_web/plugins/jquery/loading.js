function loading_nomal() {
  $(".lds-roller-div").css("display", "block");
  $(".body-content").addClass("disable-body");
  $("body").css("overflow", "hidden");
  $("#background-black").addClass('show');
  $("#background-black").addClass('modal-backdrop');
}

function clearLoading(){
  $(".lds-roller-div").css("display", "none");
  $(".body-content").removeClass("disable-body");
  $("body").css("overflow", "auto");
  $("#background-black").removeClass('show');
  $("#background-black").removeClass('modal-backdrop');
}
