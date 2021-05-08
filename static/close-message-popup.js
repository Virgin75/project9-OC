
popup = document.getElementById('popup')

console.log('js chargé')
// Le popup disparait automatiquement au bout de 2 secondes
if (popup) {
    console.log('popup chargé')
    setTimeout(
        function(){document.getElementsByClassName("message")[0].style.visibility = "hidden"},
    5000)
    
    
}