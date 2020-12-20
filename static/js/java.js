var mygeojson = $.ajax({
  url:
    "http://127.0.0.1:5000/getdata",
  dataType: "json",
  success: console.log(" data successfully loaded."),
  error: function(xhr) {
    alert(xhr.statusText);
  }
});
$.when(mygeojson).done(function() {
  function updateHTML(locating) {
    localStorage.setItem("location", locating);
    // document.getElementById("loca").innerHTML = locating;
  }

  var map = L.map("map").setView([28, 72], 4);
  
  //... adding data in searchLayer ...

  map.doubleClickZoom.disable();

  var theMarker = {};

  map.on("dblclick", function(e) {
    lat = e.latlng.lat;
    lon = e.latlng.lng;

    // console.log("You clicked the map at LAT: "+ lat+" and LONG: "+lon );
    var locating = [lat, lon];
    // document.getElementById('output').innerHTML = location;
    updateHTML(locating);

    //Clear existing marker,

    if (theMarker != undefined) {
      map.removeLayer(theMarker);
    }

    //Add a marker to show where you clicked.
    // theMarker = L.marker([lat,lon]).addTo(map).bindPopup("<h1>This is your marker</h1><br> <form action='/forms'><button type='submit'>Click me</button></form>")
    theMarker = L.marker([lat, lon])
      .addTo(map)
      .bindPopup(
        "<h1>This is your marker</h1><br> <form action='/forms'><button type='submit'>Click me</button></form>"
      );
  });

  function onEachFeature(properties, layer) {
    console.log(properties.properties.Name);
    var popupContent =
      "<p class='rock'>" +
      properties.properties.Name +
      "</p>" +
      "<audio controls src= " +
      properties.properties.Name +
      " > </audio>";
    console.log(properties.properties.recording);

    // var popupContent = "<p>" +feature.properties.Name+ "</p>" ;

    if (properties && properties.popupContent) {
      popupContent += properties.popupContent;
    }

    layer.bindPopup(popupContent);
  }

  var basemap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}
  ).addTo(map);
  // Add requested external GeoJSON to map
  var kyGeojson = L.geoJSON(mygeojson.responseJSON, {
    onEachFeature: onEachFeature
  }).addTo(map);
var searchControl = L.esri.Geocoding.geosearch().addTo(map);

      // create an empty layer group to store the results and add it to the map
      var results = L.layerGroup().addTo(map);

      // listen for the results event and add every result to the map
      searchControl.on("results", function (data) {
        results.clearLayers();
        for (var i = data.results.length - 1; i >= 0; i--) {
          // results.addLayer(L.marker(data.results[i].latlng));
        }
      });
});


      // create the geocoding control and add it to the map
      