var marker;
var map;
var area;
var initialLocation;
var browserSupportFlag = new Boolean();
var pos;

function initialize() {
    //Ustawia bierzaca pozycje
    if (navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);  //Pobranie wspolrzednych
            map.setCenter(initialLocation); //Ustawienie centrum mapy
            document.getElementById('X').value = position.coords.latitude;    //Ustawiam aktualne wartosci dla wspolrzednych
            document.getElementById('Y').value = position.coords.longitude;
            marker = new google.maps.Marker({   //Nowy marker
                map: map,
                position: initialLocation,
                icon: 'images/marker.png'
            });

            var areaOpt = { //opcje obszaru
                map: map,   //mapa
                center: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),    //pozycja
                radius: 100,    //promien
                strokeColor: '#FF0000', //kolor lini
                strokeOpacity: 0.8, //przezroczystosc lini
                strokeWeight: 2,    //grubosc lini
                fillColor: '#FF0000',   //Kolor obszaru
                fillOpacity: 0.35   //przezroczystosc obszaru
            };

            area = new google.maps.Circle(areaOpt); //Rysowanie obszaru na podstawie opcji

        }, function() {
            handleNoGeolocation(browserSupportFlag);
        });
    }
    else {
        browserSupportFlag = false;
    }

    var myOptions = {   //Opcje wyswietlania mapy
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);    //Tworzenie mapy

    google.maps.event.addListener(map, 'click', function(event){    //Ustawianie markera wraz z obszarem
        if(marker)
        {
            marker.setMap(null);
            marker = null;
            area.setMap(null);
            area = null;
        }
        var markOpt = {
            position: event.latLng,
            map: map,
            icon: "{% static 'images/marker.png' %}",
        };
        var areaOpt = { //opcje obszaru
            map: map,   //mapa
            center: event.latLng,   //pozycja
            radius: 100,    //promien
            strokeColor: '#FF0000', //kolor lini
            strokeOpacity: 0.8, //przezroczystosc lini
            strokeWeight: 2,    //grubosc lini
            fillColor: '#FF0000',   //Kolor obszaru
            fillOpacity: 0.35   //przezroczystosc obszaru
        };

        area = new google.maps.Circle(areaOpt); //Rysowanie obszaru na podstawie opcji
        marker = new google.maps.Marker(markOpt);   //Rysowanie markera
    });
}

google.maps.event.addDomListener(window, 'load', initialize);