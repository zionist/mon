(function() {
  var readCookie, setCookie;

  setCookie = function(cookieName, cookieValue) {
    var expire, today;
    today = new Date();
    expire = new Date(today.getTime() + (24 * 60 * 60 * 1000));
    return document.cookie = cookieName + "=" + escape(cookieValue) + ";expires=" + expire.toGMTString();
  };

  readCookie = function(name) {
    var c, ca, i, nameEQ;
    nameEQ = name + "=";
    ca = document.cookie.split(";");
    i = 0;
    while (i < ca.length) {
      c = ca[i];
      while (c.charAt(0) === " ") {
        c = c.substring(1, c.length);
      }
      if (c.indexOf(nameEQ) === 0) {
        return c.substring(nameEQ.length, c.length).replace(/"/g, '');
      }
      i++;
    }
    return ca;
  };

  $("form :input").on('change', function() {
    return setCookie("form_changed", "1");
  });

  $('form').submit(function() {
    setCookie("form_changed", "0");
    return void 0;
  });

  window.onbeforeunload = function() {
    if (readCookie("form_changed") === "1") {
      setCookie("form_changed", "0");
      return 'Пожалуйста проверьте что данные сохранены';
    } else {
      return void 0;
    }
  };

  $(document).ready(function() {
    if (readCookie("form_changed") === "1") {
      return setCookie("form_changed", "0");
    }
  });

}).call(this);
