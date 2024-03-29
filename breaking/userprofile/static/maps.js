var map;
var marker;
var area;
var initialLocation;

function initialize()
{
    initialLocation = new google.maps.LatLng("{{ latitude }}", "{{ longitude }}");  //Pobranie wspolrzednych
alert({{ latitude }});
    //Opcje mapy
    map = new google.maps.Map(document.getElementById("map-canvas"), {
        zoom: 16,
        center: initialLocation,
        mapTypeId: google.maps.MapTypeId.SATELLITE                
    });

    //Nowy marker
    marker = new google.maps.Marker({
        map: map,
        position: initialLocation,
        icon: "{% static 'images/marker.png' %}",
        title: 'Twoja baza'
    });

    //Nowy obszar wokol markera
    area = new google.maps.Circle({
        map: map,   //mapa
        center: new google.maps.LatLng("{{ latitude }}", "{{ longitude }}"),    //pozycja
        radius: 100,    //promien
        strokeColor: '#FF0000', //kolor lini
        strokeOpacity: 0.8, //przezroczystosc lini
        strokeWeight: 2,    //grubosc lini
        fillColor: '#FF0000',   //Kolor obszaru
        fillOpacity: 0.35   //przezroczystosc obszaru
    });


    if("{{ t_latitude }}" && "{{ t_longitude }}")   //Rysowanie okręgu dla misji użytkownka
    {
        marker = new google.maps.Marker({   //Nowy marker
            map: map,
            position: new google.maps.LatLng("{{ t_latitude }}", "{{ t_longitude }}"),
            icon: "{% static 'images/marker.png' %}",
            title: 'Twoja misja'
        });

        area = new google.maps.Circle({ //opcje obszaru
            map: map,   //mapa
            center: new google.maps.LatLng("{{ t_latitude }}", "{{ t_longitude }}"),    //pozycja
            radius: 100,    //promien
            strokeColor: '#FF0000', //kolor lini
            strokeOpacity: 0.8, //przezroczystosc lini
            strokeWeight: 2,    //grubosc lini
            fillColor: '#FF0000',   //Kolor obszaru
            fillOpacity: 0.35   //przezroczystosc obszaru
        });
    }
}

google.maps.event.addDomListener(window, 'load', initialize);