var marker;
var map;
var area;
var initialLocation;
var browserSupportFlag = new Boolean();
var pos;

function initialize() 
{
    //Ustawia bierzaca pozycje
    if (navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);  //Pobranie wspolrzednych
            map.setCenter(initialLocation); //Ustawienie centrum mapy

            document.getElementsByName('positionX')[0].value = position.coords.latitude;    //Ustawiam aktualne wartosci dla wspolrzednych
            document.getElementsByName('positionY')[0].value = position.coords.longitude;
            marker = new google.maps.Marker({   //Nowy marker
                map: map,
                position: initialLocation,
                icon: "../static/images/marker.png"
            });

            google.maps.event.addListener(map, 'click', function(event) {   //Uzytkownk ustawia swoja pozycje na mapie
                var lat = event.latLng.lat();
                var lng = event.latLng.lng();
                document.getElementsByName('positionX')[0].value = lat; //Wypisuje zaznaczone wspolrzedne
                document.getElementsByName('positionY')[0].value = lng;
                initialLocation = new google.maps.LatLng(lat, lng);
                marker.setMap(null);
                marker = new google.maps.Marker({
                    map: map,
                    position: initialLocation,
                    icon: "../static/images/marker.png"
                });
            });

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
}

google.maps.event.addDomListener(window, 'load', initialize);