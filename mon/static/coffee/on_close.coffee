setCookie = (cookieName, cookieValue) ->
   today = new Date()
   expire = new Date(today.getTime() + (24 * 60 * 60 * 1000));
   document.cookie = cookieName + "=" + escape(cookieValue) + ";expires=" + expire.toGMTString()

readCookie = (name) ->
  nameEQ = name + "="
  ca = document.cookie.split(";")
  i = 0
  while i < ca.length
    c = ca[i]
    c = c.substring(1, c.length)  while c.charAt(0) is " "
    return c.substring(nameEQ.length, c.length).replace(/"/g, '')  if c.indexOf(nameEQ) is 0
    i++
  ca

$("form :input").on 'change', ->
  setCookie("form_changed", "1")

$('form').submit ->
  setCookie("form_changed", "0")
  return undefined

window.onbeforeunload = () ->
    if readCookie("form_changed") == "1"
        setCookie("form_changed", "0")
        return 'Пожалуйста проверьте что данные сохранены'
    else
        return undefined

$(document).ready ->
  if readCookie("form_changed") == "1"
    setCookie("form_changed", "0")
