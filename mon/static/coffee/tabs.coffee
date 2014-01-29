set_active_tab = () ->
  urls = {
      "/main/$": "main"
      "/payment/payments/$": "payments",
      "/payment/payment": "payments",
      "/obj/building/": "buildings",
      "/obj/buildings/$": "buildings"
      "/obj/buildings/mo/$": "buildings"
      "/cmp/auction/": "auctions",
      "/cmp/auctions": "auctions"
      "/cmp/contract/": "contracts",
      "/cmp/contracts": "contracts"
      "/cmp/result/": "results",
      "/cmp/results": "results"
      "/imgfile/imgfile/get_select_mo_form/": "results"
      "/imgfile/imgfile/get_questions_list_form/": "results"
      "/mo/mos/$": "mos"
      "/mo/mo/\\d+/": "mos"
      "/mo/mo/update/\\d+/": "mos"
      "/mo/mo/pre_delete/\\d+/": "mos"
      "/filter/\\d+/": "filters",
      "/users/": "manage"
      "/user/user/": "manage"
      "/user/choices/": "manage"
  }
  for url_regex, div_id of urls
    m = RegExp(url_regex)
    if m.test(document.URL)
      $("#" + div_id).addClass("active")
      break

$(document).ready ->
  set_active_tab()
