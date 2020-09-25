L.mapbox.accessToken =
              "pk.eyJ1IjoicmlzaGFiaG5haWsxMjMiLCJhIjoiY2tkdHoza201MjM1OTJwdHZoNHI2NDE1diJ9.Q3ePBZyDe66tWNufCrHS5w";

            var mapboxTiles = L.tileLayer(
              "https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=" +
                L.mapbox.accessToken,
              {
                attribution:
                  '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                tileSize: 512,
                zoomOffset: -1
              }
            );


            function updateHTML( locating) {
             localStorage.setItem("location",locating);
              // document.getElementById("loca").innerHTML = locating;
            }
      

            var map = L.map("map")
              .addLayer(mapboxTiles)
              .setView([28, 72], 4);

            map.doubleClickZoom.disable();

            var theMarker = {};

        map.on('dblclick',function(e){
          lat = e.latlng.lat;
          lon = e.latlng.lng;

          // console.log("You clicked the map at LAT: "+ lat+" and LONG: "+lon );
          var locating=[lat,lon];
          // document.getElementById('output').innerHTML = location;
          updateHTML(locating);
            
      //    console.log(locating.Array)
      //       console.log(theMarker)
      // console.log(locating)
              //Clear existing marker,

              if (theMarker != undefined) {
                    map.removeLayer(theMarker);
              };

          //Add a marker to show where you clicked.
          // theMarker = L.marker([lat,lon]).addTo(map).bindPopup("<h1>This is your marker</h1><br> <form action='/forms'><button type='submit'>Click me</button></form>")
           theMarker = L.marker([lat,lon]).addTo(map).bindPopup("<h1>This is your marker</h1><br> <form action='/forms'><button type='submit'>Click me</button></form>")
      });

    


      var mygeojson = {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "properties": {
                "dialect": 11793,
                "Name": "Ram",
                },
            "geometry": {
              "type": "Point",
              "coordinates": [
                72.99316406249999,
                18.687878686034182
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {
                "dialect": 11793,
                "Name": "shyam",
                "url":"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
            "geometry": {
              "type": "Point",
              "coordinates": [
                73.916015625,
                15.919073517982426
              ]
            }
          },
          {
            "type": "Feature",
            "properties":{
                "dialect": 11793,
                "Name": "Babu Rao",
                "url":""},
            "geometry": {
              "type": "Point",
              "coordinates": [
                78.22265625,
                22.471954507739227
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {
                "dialect": 11793,
                "Name": "Rishabh",
                "url":""},
            "geometry": {
              "type": "Point",
              "coordinates": [
                75.234375,
                14.221788628397572
              ]
            }
          }
        ]
      }


      function onEachFeature(feature, layer) {
        var popupContent = "<p class='rock'>" +feature.properties.Name+ "</p>"+"<audio controls src= "+feature.properties.url+" > </audio>" ;


        // var popupContent = "<p>" +feature.properties.Name+ "</p>" ;


        if (feature.properties && feature.properties.popupContent) {
            popupContent += feature.properties.popupContent;
        }

        layer.bindPopup(popupContent);
    }

    L.geoJson(mygeojson,{onEachFeature: onEachFeature}).addTo(map);


