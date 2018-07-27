sticky = 0;
var tmpNewLocationList = {};
var tmpNewBinList = {};


window.onload = function () {
    let navbar = document.getElementById("navbar");
    sticky = navbar.offsetTop;
    window.onscroll = function () { myFunction() };
    let addLocationButton = document.getElementById('js_location_add');
    let removeLocationButton = document.getElementById('js_location_remove');
    let addBinButton = document.getElementById('js_bin_add');
    let removeBinButton = document.getElementById('js_bin_remove');
    addBinButton.addEventListener("click", onAddBinButtonClick);
    removeBinButton.addEventListener("click", onRemoveBinButtonClick);
    addLocationButton.addEventListener("click", onAddLocationButtonClick);
    removeLocationButton.addEventListener("click", onRemoveLocationButtonClick);
}

function serializeLocations() {
    let string = "";
    let array = [];
    for (const [k, v] of Object.entries(tmpNewLocationList)) {
        array.push(v);
    }
    //Now let's get the element that will hold our json:
    let element = document.getElementById("submit_locations");
    element.value = JSON.stringify(array);
}

function serializeBins() {
    let string = "";
    let array = [];
    for (const [k, v] of Object.entries(tmpNewBinList)) {
        array.push(v);
    }
    //Now let's get the element that will hold our json:
    let element = document.getElementById("submit_bins");
    element.value = JSON.stringify(array);
}

function onRemoveLocationButtonClick(self) {
    let location_element = document.getElementById('js_locations');
    let locations_added_list = document.getElementById('js_location_list');
    listItems = locations_added_list.querySelectorAll("li");
    for (i = 0; i < listItems.length; i++) {
        let checkbox = listItems[i].querySelector("input");
        if (checkbox.checked == true) {
            delete tmpNewLocationList[listItems[i].id]
            locations_added_list.removeChild(listItems[i]);
        }
    }
    serializeLocations();
}

function onAddLocationButtonClick(self) {
    let location_element = document.getElementById('js_locations');
    let locations_added_list = document.getElementById('js_location_list');
    let listItem = document.createElement("li");
    listItem.id = location_element.value;
    let listItemCheckbox = document.createElement("input");
    listItemCheckbox.type = "checkbox";
    let listItemText = document.createTextNode(location_element.options[location_element.selectedIndex].innerHTML);
    if (!document.getElementById(listItem.id)) {
        tmpNewLocationList[listItem.id] = listItem.id
        //Now append them:
        listItem.appendChild(listItemCheckbox);
        listItem.appendChild(listItemText);
        locations_added_list.appendChild(listItem);
    }
    serializeLocations();
}

function onRemoveBinButtonClick(self) {
    let bin_element = document.getElementById('js_bins');
    let bins_added_list = document.getElementById('js_bin_list');
    listItems = bins_added_list.querySelectorAll("li");
    for (i = 0; i < listItems.length; i++) {
        let checkbox = listItems[i].querySelector("input");
        if (checkbox.checked == true) {
            delete tmpNewBinList[listItems[i].id]
            bins_added_list.removeChild(listItems[i]);
        }
    }
    serializeBins();
}

function onAddBinButtonClick(self) {
    let bin_element = document.getElementById('js_bins');
    let bins_added_list = document.getElementById('js_bin_list');
    let listItem = document.createElement("li");
    listItem.id = bin_element.value;
    let listItemCheckbox = document.createElement("input");
    listItemCheckbox.type = "checkbox";
    let listItemText = document.createTextNode(bin_element.options[bin_element.selectedIndex].innerHTML);
    if (!document.getElementById(listItem.id)) {
        tmpNewBinList[listItem.id] = listItem.id
        //Now append them:
        listItem.appendChild(listItemCheckbox);
        listItem.appendChild(listItemText);
        bins_added_list.appendChild(listItem);
    }
    serializeBins();
}

function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
}
