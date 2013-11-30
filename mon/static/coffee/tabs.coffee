set_active_tab = () ->
  urls = {
      "/main/$": "main"
      "/obj/building/\\D+/$": "buildings",
      "/obj/buildings/$": "buildings"
      "/cmp/auction/\\D+/$": "auctions",
      "/cmp/auctions/$": "auctions"
      "/cmp/contract/\\D+/$": "contracts",
      "/cmp/contracts/$": "contracts"
      "/cmp/result/\\D+/$": "results",
      "/cmp/results/$": "results"
  }
  for url_regex, div_id of urls
    m = RegExp(url_regex)
    if m.test(document.URL)
      $("#" + div_id).addClass("active")
      break

$(document).ready ->
  set_active_tab()
