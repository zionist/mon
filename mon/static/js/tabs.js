(function() {
  var set_active_tab;

  set_active_tab = function() {
    var div_id, m, url_regex, urls, _results;
    urls = {
      "/main/$": "main",
      "/obj/building/\\D+/$": "buildings",
      "/obj/buildings/$": "buildings",
      "/cmp/auction/\\D+/$": "auctions",
      "/cmp/auctions/$": "auctions",
      "/cmp/contract/\\D+/$": "contracts",
      "/cmp/contracts/$": "contracts",
      "/cmp/result/\\D+/$": "results",
      "/cmp/results/$": "results"
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
