$(document).ready ->
  set_masks = () ->
    $(".date_mask").mask("99.99.9999")
    $(".date_time_mask").mask("99.99.9999 99:99")
    return undefined
  set_masks()
