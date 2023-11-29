function Open_my_Dialog() {
    var dialog_tab = document.getElementById("myDialog");

    dialog_tab.show();
    setTimeout(() => dialog_tab.close(), 1500);

        // dialog_tab.close();
}