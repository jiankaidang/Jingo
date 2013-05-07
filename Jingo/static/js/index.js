var map, fakeMarker, uid = $("#uid").val(), bouncingMarker, infoWindow;
function initialize() {
    var mapOptions = {
        zoom: 16,
        streetViewControl: false,
        mapTypeControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    fakeMarker = new google.maps.Marker({
        clickable: false,
        icon: {
            url: '/static/img/jingo.gif',
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(25, 25)
        },
        shadow: null,
        zIndex: 999,
        map: map,
        animation: google.maps.Animation.BOUNCE,
        draggable: true,
        visible: false
    });
    google.maps.event.addListener(fakeMarker, 'dragend', function (event) {
        fakeMarker.setPosition(event.latLng);
        fakeMarker.setVisible(true);
        receiveNotes(event.latLng);
        $(".top-bar,#note-form").show();
    });
    google.maps.event.addListener(map, 'click', function (event) {
        fakeMarker.setPosition(event.latLng);
        fakeMarker.setVisible(true);
        receiveNotes(event.latLng);
        $(".top-bar,#note-form").show();
    });
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
            receiveNotes(pos);
        }, function () {
            handleNoGeolocation(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }
}

function handleNoGeolocation(errorFlag) {
}

google.maps.event.addDomListener(window, 'load', initialize);
$("#setToCurrentLocation").click(function () {
    navigator.geolocation.getCurrentPosition(function (position) {
        var pos = new google.maps.LatLng(position.coords.latitude,
            position.coords.longitude);
        map.setCenter(pos);
        fakeMarker.setVisible(false);
        receiveNotes(new google.maps.LatLng(position.coords.latitude,
            position.coords.longitude));
    });
    return false;
});
$("#publishNote").click(function () {
    var noteInput = $("#note");
    if (noteInput.val() == "") {
        return false;
    }
    getMarkerPosition(function (latLng) {
        $("#n_latitude").val(latLng.lat());
        $("#n_longitude").val(latLng.lng());
        $.post("/tasks/postNote/", $("#note-form").serialize(), function (data) {
            $("#note-form")[0].reset();
            dropMarker({
                noteid: data.noteid,
                n_latitude: latLng.lat(),
                n_longitude: latLng.lng()
            });
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
$("#searchBtn").click(function () {
    getMarkerPosition(function (latLng) {
        $.post("/tasks/searchNotes/", {
            uid: uid,
            keywords: $("#searchMaps").val(),
            u_latitude: latLng.lat(),
            u_longitude: latLng.lng()
        }, function (data) {
            $("#searchMaps").val("");
            renderNoteList(data);
        });
    });
});
var markersArray = [];
function renderNoteList(data) {
    $.each(markersArray, function (index, marker) {
        marker.setMap(null);
    });
    $.each(data.noteslist, function (index, note) {
        dropMarker(note);
    });
}
function receiveNotes(latLng) {
    $.post("/tasks/receiveNotes/", {
        uid: uid,
        u_latitude: latLng.lat(),
        u_longitude: latLng.lng()
    }, renderNoteList);
}
function getMarkerPosition(callback) {
    if (fakeMarker.getVisible()) {
        callback(fakeMarker.getPosition());
        return;
    }
    navigator.geolocation.getCurrentPosition(function (position) {
        callback(new google.maps.LatLng(position.coords.latitude,
            position.coords.longitude));
    });
}
function dropMarker(note) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(note.n_latitude, note.n_longitude),
        map: map,
        animation: google.maps.Animation.DROP
    });
    markersArray.push(marker);
    google.maps.event.addListener(marker, 'click', function () {
        if (bouncingMarker) {
            infoWindow.close();
            bouncingMarker.setAnimation(null);
        }
        bouncingMarker = marker;
        $(".top-bar,#note-form").hide();
        marker.setAnimation(google.maps.Animation.BOUNCE);
        $.post("/tasks/readNote/", {
            noteid: note.noteid
        }, function (data) {
            infoWindow = new google.maps.InfoWindow({
                content: $(data)[0]
            });
            google.maps.event.addListener(infoWindow, 'domready', function () {
                var content = $(infoWindow.getContent());
                content.on("click", ".note-comment-button",function () {
                    var container = $(this).closest(".note-container");
                    container.animate({
                        scrollTop: container.find(".note-comments-container").show().position().top + 1
                    });
                }).on("click", ".publish-comment-btn",function () {
                        var publishCommentBtn = $(this);
                        var commentsNum = publishCommentBtn.closest(".note-container").find(".comments-num"),
                            noteCommentTextarea = publishCommentBtn.prev(".note-comment-textarea");
                        var comment = noteCommentTextarea.val(),
                            commentsList = publishCommentBtn.closest(".note-comments-container").find(".comments-list");
                        getMarkerPosition(function (latLng) {
                            $.post("/tasks/postComment/", {
                                uid: uid,
                                noteid: note.noteid,
                                c_latitude: latLng.lat(),
                                c_longitude: latLng.lng(),
                                comment: comment
                            }, function (data) {
                                commentsList.prepend('<dt>' + data.u_name + '</dt><dd>' + comment +
                                    '</dd><p class="muted">' + data.c_timestamp + '</p>');
                                commentsNum.html(parseInt(commentsNum.html()) + 1);
                                noteCommentTextarea.val("");
                            });
                        });
                    }).css({
                        maxHeight: content.height()
                    }).on("click", ".note-like-button",function () {
                        var likesNum = $(this).closest(".note-container").find(".likes-num");
                        $.post("/tasks/clickLike/", {
                            noteid: note.noteid
                        }, function (data) {
                            likesNum.html(data.n_like);
                        });
                    }).on("click", ".follow-friend",function () {
                        var followFriendBtn = $(this), requestPendingBtn = followFriendBtn.next(".request-pending");
                        $.post("/tasks/sendInvitation/", {
                            uid: uid,
                            f_uid: $(this).closest(".note-container").attr("poster-uid")
                        }, function () {
                            followFriendBtn.hide();
                            requestPendingBtn.show();
                        });
                    }).on("click", ".unfollow-friend", function () {
                        var unfollowFriendBtn = $(this), followFriendBtn = unfollowFriendBtn.prev(".follow-friend");
                        $.post("/tasks/unfollow/", {
                            uid: uid,
                            f_uid: $(this).closest(".note-container").attr("poster-uid")
                        }, function () {
                            unfollowFriendBtn.hide();
                            followFriendBtn.show();
                        });
                    });
            });
            google.maps.event.addListener(infoWindow, 'closeclick', function () {
                $(".top-bar,#note-form").show();
                marker.setAnimation(null);
            });
            infoWindow.open(map, marker);
        });
    });
}
if ($("#note-bar").attr("data-n-request")) {
    setInterval(function () {
        $(".icon-heart").toggleClass("icon-white");
    }, 500);
}