var map;

function initialize() {
    var mapOptions = {
        zoom: 13,
        streetViewControl: false,
        mapTypeControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    // Try HTML5 geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            map.setCenter(pos);
        }, function () {
            handleNoGeolocation(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }
    var myloc = new google.maps.Marker({
        clickable: false,
        icon: new google.maps.MarkerImage('http://maps.gstatic.com/mapfiles/mobile/mobileimgs2.png',
            new google.maps.Size(22, 22),
            new google.maps.Point(0, 18),
            new google.maps.Point(11, 11)),
        shadow: null,
        zIndex: 999,
        map: map
    });

    if (navigator.geolocation) navigator.geolocation.getCurrentPosition(function (pos) {
        var me = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
        myloc.setPosition(me);
    }, function (error) {
        // ...
    });
}

function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
        var content = 'Error: The Geolocation service failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }

    var options = {
        map: map,
        position: new google.maps.LatLng(60, 105),
        content: content
    };

    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

google.maps.event.addDomListener(window, 'load', initialize);
$("#setToCurrentLocation").click(function () {
    navigator.geolocation.getCurrentPosition(function (position) {
        var pos = new google.maps.LatLng(position.coords.latitude,
            position.coords.longitude);
        map.setCenter(pos);
    });
    return false;
});
$("#publishNote").click(function () {
    var noteInput = $("#note");
    navigator.geolocation.getCurrentPosition(function (position) {
        $.post("/tasks/postNote/", {
            uid: $(this).attr("data-uid"),
            note: noteInput.val(),
            n_latitude: position.coords.latitude,
            n_longitude: position.coords.longitude
        }, function () {
            noteInput.val("");
        });
    });
    return false;
});
$("#noteDetail").click(function () {
    $(this).find("i").toggleClass("icon-chevron-up").toggleClass("icon-chevron-down");
    return false;
});