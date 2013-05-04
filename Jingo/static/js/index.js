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
    // Try HTML5 geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            map.setCenter(pos);
            myloc.setPosition(pos);

            $.post("/tasks/receiveNotes/", {
                uid: $("#uid").val(),
                u_latitude: position.coords.latitude,
                u_longitude: position.coords.longitude
            }, function (data) {
                $.each(data.noteslist, function (index, note) {
                    var marker = new google.maps.Marker({
//                position: new google.maps.LatLng(note.n_latitude, note.n_longitude),
                        position: pos,
                        map: map
                    });
                    google.maps.event.addListener(marker, 'click', function () {
                        $(".top-bar,#note-form").hide();
//                        $.post("/tasks//", {
//
//                        }, function (data) {
                        new google.maps.InfoWindow({
                            content: '<div class="container note-container"><div>Jiankai Dang<button class="btn btn-mini follow-friend" type="button">Follow</button>' +
                                '<button class="btn btn-mini follow-friend btn-danger" type="button">Unfollow</button></div><div><span class="muted note-time">04/30/2013 08:35 PM</span>' +
                                '<i class="icon-globe"></i><i class="icon-user"></i><i class="icon-lock"></i></div>' +
                                '<p>abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, abcdefgd, ' +
                                '<br><a href="http://google.com">http://google.com</a></p>' +
                                '<div class="muted"><span class="note-action-num">47 Likes</span><span class="note-action-num">47 Comments</span></div>' +
                                '<div><button class="btn btn-mini note-button"><i class="icon-thumbs-up"></i> Like</button>' +
                                '<button class="btn btn-mini note-button note-comment-button"><i class="icon-comment"></i> Comment</button></div>' +
                                '<div class="note-comments-container"><div class="control-group"><div class="controls"><div class="input-append">' +
                                '<textarea placeholder="Write a comment..." rows="1" required class="note-comment-textarea"></textarea>' +
                                '<a class="add-on" href="#"><i class="icon-share"></i></a></div></div></div></div>' +
                                '</div>'
                        }).open(map, marker);
//                        });
                    });
                });
            });
        }, function () {
            handleNoGeolocation(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }
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
    var newTagLi = $('<li><input type="text" pattern="[a-zA-Z]+"></li>').prependTo(sysTagLi.find("ul"));
    newTagLi.find("input").blur(function () {
        var tagName = $(this).val();
        if (!tagName) {
            newTagLi.remove();
            return;
        }
        newTagLi.html('<label class="checkbox"><input type="checkbox" value="' +
            $(this).closest(".sys-tag-container").attr("data-tagid") + "_" + tagName + '" name="tag_names" class="customized-tag">' + tagName +
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
$("#map-canvas").on("click", ".note-comment-button", function () {
    $(this).closest(".note-container").find(".note-comments-container").slideUp();
});