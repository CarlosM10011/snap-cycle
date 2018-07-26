sticky = 0;
var zipCode;
var theMap;
var markers=[];
var theLat;
var theLng;

window.onload = function () {

    let navbar = document.getElementById("navbar");
    sticky = navbar.offsetTop;
    window.onscroll = function () { myFunction() };

    zipCode = document.getElementById('zip_box');
    // zipCode.onclick = myMap;

    myMap();

    let goButton = document.getElementById('go');
    console.log(goButton);
    goButton.addEventListener("click", onGoButton);
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
  // google.maps.event.addListener(marker, 'click', infoWindow);
  // console.log("marker clicked");
  // var elt = document.getElementById("map");
  console.log(markers);
}
//
// function infoWindow(self){
//   console.log("inside infoWindow");
// }

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
