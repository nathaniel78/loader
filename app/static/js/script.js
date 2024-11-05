$(document).ready(function(){
    $('#host_ip').mask('099.099.099.099');

    setTimeout(function() {
      $(".alert").fadeOut("slow", function(){
        $(this).alert('close');
      });
    }, 3000);
  });