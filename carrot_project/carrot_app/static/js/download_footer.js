document.addEventListener('DOMContentLoaded', function () {
    var appStoreButtonFooter = document.getElementById('appStoreButtonFooter');
    var googlePlayButtonFooter = document.getElementById('googlePlayButtonFooter');


    appStoreButtonFooter.addEventListener('click', function () {
        window.location.href = 'https://apps.apple.com/kr/app/당근/id1018769995'; // footer.html button
    });

    googlePlayButtonFooter.addEventListener('click', function () {
        window.location.href = 'https://play.google.com/store/apps/details?id=com.towneers.www';// main.html img button
    });

});
