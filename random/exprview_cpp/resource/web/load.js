"use strict";

var placeholder = document.getElementById("placeholder");

function updateError(text) {
    placeholder.style.visibility = "hidden";
    placeholder.innerHTML = text;
    placeholder.classList.add("error");
    placeholder.classList.remove("tree");
    placeholder.style.visibility = "visible";
}

function updateTree(text) {
    placeholder.style.visibility = "hidden";
    placeholder.innerHTML = text;
    placeholder.classList.add("tree");
    placeholder.classList.remove("error");
    placeholder.style.visibility = "visible";
}

new QWebChannel(
    qt.webChannelTransport,
    function(channel) {
        var error_handler = channel.objects.error_handler,
            tree_handler = channel.objects.tree_handler;
        updateError(error_handler.text);
        error_handler.textChanged.connect(updateError);
        tree_handler.treeChanged.connect(updateTree);
    }
);
