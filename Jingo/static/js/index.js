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
    if (noteInput.val() == "") {
        return false;
    }
    navigator.geolocation.getCurrentPosition(function (position) {
        $("#n_latitude").val(position.coords.latitude);
        $("#n_longitude").val(position.coords.longitude);
        $.post("/tasks/postNote/", $("#note-form").serialize(), function () {
            $("#note-form")[0].reset();
        });
    });
    return false;
});
$("#noteDetailTrigger").click(function () {
    $(this).find("i").toggleClass("icon-chevron-up").toggleClass("icon-chevron-down");
    $("#note-detail").slideToggle();
    return false;
});
$("#accordion2").on("click", ".add-tag",function () {
    var sysTagLi = $(this).closest("li"), tagid = sysTagLi.attr("data-tagid");
    var newTagLi = $('<li><input type="text" required></li>').prependTo(sysTagLi.find("ul"));
    newTagLi.find("input").blur(function () {
        var tagName = $(this).val();
        if (!tagName) {
            newTagLi.remove();
            return;
        }
        newTagLi.html('<label class="checkbox"><input type="checkbox" value="' + tagName + '" name="tag_names" class="customized-tag">' + tagName +
            '<a href="javascript:void(0);" class="pull-right remove-tag"><i class="icon-trash"></i></a>' +
            '</label>').find("input").click();
    }).focus();
}).on("click", ".remove-tag",function () {
        var tagLi = $(this).closest("li").remove();
    }).on("click", ".customized-tag",function () {
        if ($(this).is(":checked")) {
            $(this).closest(".sys-tag-container").find(".sys-tag").prop("checked", true);
        }
    }).on("click", ".sys-tag", function () {
        if (!$(this).is(":checked")) {
            $(this).closest(".sys-tag-container").find(".customized-tag").prop("checked", false);
        }
    });