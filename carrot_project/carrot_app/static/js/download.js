document.addEventListener('DOMContentLoaded', function () {
    var appStoreButton = document.getElementById('appStoreButton');
    var googlePlayButton = document.getElementById('googlePlayButton');
    var appStoreButtonFooter = document.getElementById('appStoreButtonFooter');
    var googlePlayButtonFooter = document.getElementById('googlePlayButtonFooter');

    appStoreButton.addEventListener('click', function () {
        window.location.href = 'https://apps.apple.com/kr/app/당근/id1018769995'; // main.html img button
    });

    googlePlayButton.addEventListener('click', function () {
        window.location.href = 'https://play.google.com/store/apps/details?id=com.towneers.www';// main.html img button
    });

    appStoreButtonFooter.addEventListener('click', function () {
        window.location.href = 'https://apps.apple.com/kr/app/당근/id1018769995'; // footer.html button
    });

    googlePlayButtonFooter.addEventListener('click', function () {
        window.location.href = 'https://play.google.com/store/apps/details?id=com.towneers.www';// main.html img button
    });

});
