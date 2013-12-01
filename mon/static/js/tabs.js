(function() {
  var set_active_tab;

  set_active_tab = function() {
    var div_id, m, url_regex, urls, _results;
    urls = {
      "/main/$": "main",
      "/obj/building/": "buildings",
      "/obj/buildings/$": "buildings",
      "/cmp/auction/": "auctions",
      "/cmp/auctions/$": "auctions",
      "/cmp/contract/": "contracts",
      "/cmp/contracts/$": "contracts",
      "/cmp/result/": "results",
      "/cmp/results/$": "results",
      "/mo/mos/$": "mos",
      "/mo/mo/": "mos",
      "/filter/\\d+/": "filters"
    };
    _results = [];
    for (url_regex in urls) {
      div_id = urls[url_regex];
      m = RegExp(url_regex);
      if (m.test(document.URL)) {
        $("#" + div_id).addClass("active");
        break;
      } else {
        _results.push(void 0);
      }
    }
    return _results;
  };

  $(document).ready(function() {
    return set_active_tab();
  });

}).call(this);
