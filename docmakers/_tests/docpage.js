/**
 * Gloabal page settings
 */
const docPage = {
    pagelogo: null,   // Page logo as an HTML tag.
    contents: null,   // Global table of contents.
    homepage: null,   // Path to the homepage.
    tocanchorsID: []  // IDs of TOC anchors
}

/**
 * Widgets on the top panel.
 * Order of widgets on the panel: 
 * contents | bookmark | homepage 
 */
const widgets = {
    contents: null,
    bookmark: null,
    homepage: null,
}

widgets.contents = `<svg class="svg-widget" width="25" height="25" viewbox="0 0 30 30">
<rect x="0" y="0" width="30" height="30" rx="7" />
<g fill="white">
    <circle cx="7" cy="8" r="2" />
    <circle cx="7" cy="15" r="2" />
    <circle cx="7" cy="22" r="2" />
</g>
<g stroke="white" stroke-width="3">
    <line x1="12" y1="8" x2="23" y2="8" />
    <line x1="12" y1="15" x2="23" y2="15" />
    <line x1="12" y1="22" x2="23" y2="22" />
</g>
</svg>`;

widgets.bookmark = `<svg class="svg-widget" width="25" height="25" viewbox="0 0 30 30">
<rect x="1" y="1" width="28" height="20" rx="7" />
<path d="M 1 10 v 20 q 14 -7 28 0 v -20" />
<g stroke="white" stroke-width="3" stroke-linecap="round">
    <line x1="9" y1="10" x2="21" y2="10" />
    <line x1="9" y1="17" x2="21" y2="17" />
</g>
</svg>`;

widgets.homepage = `<svg class="svg-widget" width="30" height="25" viewbox="0 0 36 30">
<rect x="6" y="10" width="24" height="10" rx="0" />
<rect x="6" y="15" width="24" height="15" rx="2" />
<path d="M 18 2 l 16 10 l -16 0 l -16 0 l 16 -10" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
<rect x="15" y="20" width="6" height="10" rx="0" fill="white" />
</svg>`;

/**
 * Sets up the docpage.
 */
function setDocPage() {
    setWidgets();
    setPageSettings();
    setTitleBox();
    setTocBoxes();
    setTocAnchors();
}

/**
 * Adds widgets to the docpage.
 */
function setWidgets() {
    document.getElementById("global-toc-btn").innerHTML = widgets.contents;
    document.getElementById("local-toc-btn").innerHTML = widgets.bookmark;
    document.getElementById("home-page-btn").innerHTML = widgets.homepage;
}

/**
 * Sets up the page settings.
 */
function setPageSettings() {
    if (docPage.pagelogo) {
        document.getElementById("page-logo").innerHTML = docPage.pagelogo;
    }
    if (docPage.contents) {
        document.getElementById("global-toc-box__text").innerHTML = docPage.contents;
    }
    if (docPage.contents == '') {
        document.getElementById("global-toc-box").style.display = 'none';
        document.getElementById("global-toc-btn").style.display = 'none';
    }
    if (docPage.homepage == '') {
        document.getElementById("home-page-btn").style.display = 'none';
    }
}

/**
 * Sets up the title box.
 */
function setTitleBox() {

    let title = document.getElementById('title-box__title');
    let annot = document.getElementById('title-box__annotation');

    if (title.innerHTML == '' && annot.innerHTML == '') {
        document.getElementById('title-box').style.display = 'none';
    }

}

/**
 * Sets up the visibility of TOC boxes depending on the screen width.
 */
function setTocBoxes() {
    if (window.innerWidth < 1000) {
        document.getElementById("global-toc-box").style.visibility = "hidden";
        document.getElementById("local-toc-box").style.visibility = "hidden";
    } else {
        document.getElementById("global-toc-box").style.visibility = "visible";
        document.getElementById("local-toc-box").style.visibility = "visible";
    }
}

/**
 * Sets up TOC anchors.
 */
function setTocAnchors() {

    extractTocAnchorsID();

    if (docPage.tocanchorsID.length == 0) {
        document.getElementById("local-toc-box").style.display = 'none';
        document.getElementById("local-toc-btn").style.display = 'none';
        return;
    }

    setTocAnchorsID();

}

/**
 * Extacts links to the TOC anchors from the local TOC.
 */
function extractTocAnchorsID() {

    let toc = document.getElementById("local-toc-box__text");
    let atags = toc.getElementsByTagName("a");

    if (atags.length == 0) {
        return null;
    }

    for (let i = 0; i < atags.length; i++) {
        docPage.tocanchorsID[i] = atags[i].href.split('#')[1];
    }

    return;

}

/**
 * Assigns IDs to TOC anchors in the document.
 */
function setTocAnchorsID() {

    let tocAnchors = document.getElementsByClassName("toc-anchor");

    if (tocAnchors.length != docPage.tocanchorsID.length) {
        return;
    }

    for (let i = 0; i < tocAnchors.length; i++) {
        tocAnchors[i].id = docPage.tocanchorsID[i];
    }

    return;

}

/**
 * Closes a local/global TOC box on the button click.
 * @param xmark The cross button in a local/global TOC box.
 */
function closeTOC(xmark) {
    xmark.parentElement.parentElement.style.visibility = "hidden";
}

/**
 * Opens/closes a local/global TOC on the button click.
 * @param btn The local/global TOC button on the top panel.
 */
function switchTOC(btn) {

    let box = document.getElementById(btn.id.replace("-btn", "-box"));

    if (box.style.visibility == "hidden") {
        box.style.visibility = "visible";
    } else {
        box.style.visibility = "hidden";
    }

}

/**
 * Navigates to the home page when the 
 * user clicks on the home page button.
 */
function gotoHomePage() {
    if (docPage.homepage) {
        window.location = docPage.homepage;
    } else {
        location.reload();
    }
}

/**
 * Assignment of the page settings.
 */

docPage.pagelogo = `<div><h3>DOC-LOGO</h3></div>`;
docPage.contents = `<p>
<ul>
    <li><a class="global-toc__top-item" href="alfa.html">Alfa</a>
        <ul>
            <li><a href="bravo.html">Bravo</a>
                <ul>
                    <li><a href="" style="pointer-events: none;">Delta</a></li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
</p>`;
docPage.homepage = `index.html`;