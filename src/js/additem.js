sticky = 0;
var zipCode;
var theMap;
var markers=[];
var theLat;
var theLng;
var tmpNewLocationList = {};
var tmpNewBinList = {};


window.onload = function () {
console.log("test")
    let navbar = document.getElementById("navbar");
    sticky = navbar.offsetTop;
    window.onscroll = function () { myFunction() };

    zipCode = document.getElementById('zip_box');
    // zipCode.onclick = myMap;

    //myMap();

    
    let addLocationButton = document.getElementById('js_location_add');
    let removeLocationButton = document.getElementById('js_location_remove');
    console.log(addLocationButton);
    let addBinButton = document.getElementById('js_bin_add');
    let removeBinButton = document.getElementById('js_bin_remove');
    addBinButton.addEventListener("click", onAddBinButtonClick);
    removeBinButton.addEventListener("click", onRemoveBinButtonClick);
    var tmpNewLocationList = {};
    addLocationButton.addEventListener("click", onAddLocationButtonClick);
    removeLocationButton.addEventListener("click", onRemoveLocationButtonClick);
}

function serializeLocations() {
    let string = "";
    let array = [];
    for (const [k, v] of Object.entries(tmpNewLocationList)) {
        array.push(v);
    }
    console.log(array);
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
    console.log(array);
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
    console.log("Add Location Button clicked.");
    let location_element = document.getElementById('js_locations');
    let locations_added_list = document.getElementById('js_location_list');
    let listItem = document.createElement("li");
    listItem.id = location_element.value;
    let listItemCheckbox = document.createElement("input");
    listItemCheckbox.type = "checkbox";
    let listItemText = document.createTextNode(location_element.innerText);
    if (!document.getElementById(listItem.id)) {
        tmpNewLocationList[listItem.id] = listItem.id
        //Now append them:
        listItem.appendChild(listItemCheckbox);
        listItem.appendChild(listItemText);
        locations_added_list.appendChild(listItem);
    }
    console.log(location_element.innerText);
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
    console.log("Add Bin Button clicked.");
    let bin_element = document.getElementById('js_bins');
    let bins_added_list = document.getElementById('js_bin_list');
    let listItem = document.createElement("li");
    listItem.id = bin_element.value;
    let listItemCheckbox = document.createElement("input");
    listItemCheckbox.type = "checkbox";
    let listItemText = document.createTextNode(bin_element.innerText);
    if (!document.getElementById(listItem.id)) {
        tmpNewBinList[listItem.id] = listItem.id
        //Now append them:
        listItem.appendChild(listItemCheckbox);
        listItem.appendChild(listItemText);
        bins_added_list.appendChild(listItem);
    }
    console.log(bin_element.innerText);
    serializeBins();
}

function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
}
// navigator.geolocation.getCurrentPosition()
console.log("hey");

function initMap() {
    // map = new google.maps.Map(document.getElementById('map'), {
    //     center: { lat: -34.397, lng: 150.644 },
    //     zoom: 8
    // });
    infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            infoWindow.open(map);
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

}

function myMap() {
  console.log('MYMAP');
  console.log(zipCode);
  // map = new google.maps.Map(document.getElementById('map'),{
  //   center:pyrmont,
  //   zoom: 15
  // });

  var mapProp= {
      center: new google.maps.LatLng(51.508742,-0.120850),
      zoom:10,
  };

  var elt = document.getElementById("map");
  console.log(elt);
  theMap = new google.maps.Map(elt,mapProp);

}

function onGoButton(self){
  console.log("Go button clicked");

  if(markers.length > 0){
    clearMarkers();
  }

  console.log(zipCode.value);
  var geocoder = new google.maps.Geocoder();

  var request={
    'address': zipCode.value,
  };

  geocoder.geocode(request, geocodingCallback);
  // var seattle = new google.maps.LatLng(47.62, -122.33);

  // var request={
  //   location: seattle,
  //   radius: '500',
  //   query: '98223',
  // };
  console.log("pass");

}


function clearMarkers(self){
  setMapOnAll();
}

function setMapOnAll(theMap){
  for(let i = 0; i < markers.length; i++){
    markers[i].setMap(map);
  }
}

function geocodingCallback(results, status){
  console.log("geocodingCallback result");
  console.log(results);
  theLat = results[0].geometry.location.lat();
  theLng = results[0].geometry.location.lng();
  console.log(theLat, theLng);

  var searchMap = new google.maps.places.PlacesService(theMap);
  theMap.setCenter(new google.maps.LatLng(theLat, theLng));
  let re = new google.maps.LatLng(theLat,theLng);
  console.log(theLat,theLng);

  var location={
    location: re,
    // radius: "500",
    query: "recycling, compost, e waste",
    rankby: "distance",
  };
  searchMap.textSearch(location, searchCallback);
  // for(let p = 0; p < location['query'].length; p++){
  //   searchMap.textSearch(location[p], searchCallback);
  // }
}

function searchCallback(results, status){
  console.log(results);
  for(let i = 0; i < results.length; i++){
    var lat = results[i].geometry.location.lat();
    var lng = results[i].geometry.location.lng();
    var position = {'lat': lat, 'lng': lng};
    var marker = new google.maps.Marker({'position': position, 'map': theMap});
    markers.push(marker);
  }
  // var elt = document.getElementById("map");
  console.log(markers);
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}


// map = new google.maps.Map(document.getElementById('map')){
//   center: pyrmont,
//   zoom: 15
// }
//
// map = new google.maps.Map(document.getElementById('map')){
//   center: {lat: },
//   zoom: 15
// }
