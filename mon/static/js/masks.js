(function() {
  $(document).ready(function() {
    var set_masks;
    return set_masks = function() {
      $(".date_mask").mask("99.99.9999");
      $(".date_time_mask").mask("99.99.9999 99:99");
      return void 0;
    };
  });

  $(document).ready(function() {
    return set_masks();
  });

}).call(this);
