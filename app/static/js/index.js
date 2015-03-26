$( window ).load(function() {
  $('a.deletebutton').click(function(){
    if (confirm("Are you sure you want to delete this report?")) {
      return true;
    }
    return false;
  });
});