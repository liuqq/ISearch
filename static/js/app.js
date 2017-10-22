function makeUL(lst) {
    var html = [];
    html.push('<ul>');
    $(lst).each(function() { html.push(makeLI(this)) });
    html.push('</ul>');
    return html.join("\n");
}

function makeLI(elem) {
    var html = [];
    html.push('<li>');
    html.push(elem.name);
    if (elem.link)
        html.push('<a>' + elem.link + '</a>');
    if (elem.sub)
        html.push('<div>' + makeUL(elem.sub) + '</div>');
    html.push('</li>');
    return html.join("\n");
}

$(function() {
    $("body").html(makeUL(JSON.Root));
    var myjson = {{json_res}};
    console.log(myjson);
});

