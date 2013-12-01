set_active_tab = () ->
  urls = {
      "/main/$": "main"
      "/obj/building/": "buildings",
      "/obj/buildings/$": "buildings"
      "/cmp/auction/": "auctions",
      "/cmp/auctions/$": "auctions"
      "/cmp/contract/": "contracts",
      "/cmp/contracts/$": "contracts"
      "/cmp/result/": "results",
      "/cmp/results/$": "results"
      "/mo/mos/$": "mos"
      "/filter/\\d+/": "filters",
  }
  for url_regex, div_id of urls
    m = RegExp(url_regex)
    if m.test(document.URL)
      $("#" + div_id).addClass("active")
      break

$(document).ready ->
  set_active_tab()
