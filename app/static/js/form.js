$( window ).load(function() {
  //Fallback for IE9 not supporting the 'formaction' attribute on the submit buttons.
  $('form#shift_report_form').on('click', 'input[type=submit]', function (e) {
      var attr = this.getAttribute('formaction');
      if (attr) {
          $('form#shift_report_form').action = attr;
      }
  });
});