/**
 * Author: Jiankai Dang
 * Date: 4/25/13
 * Time: 11:49 PM
 */
$(function () {
    var headingClass = ".accordion-heading", profileContainer = $("#accordion2").on("click", ".icon-pencil",function () {
        var heading = $(this).closest(headingClass);
        heading.find("a").hide();
        heading.find("input").show().focus();
    }).on("blur", "input",function () {
            var heading = $(this).closest(headingClass);
            heading.find("a").show();
            var stateNameInput = heading.find("input:text").hide(), stateName = stateNameInput.val();
            $.post("/tasks/updateState/", {
                uid: heading.attr("data-uid"),
                stateid: heading.attr("data-state-id"),
                state_name: stateName
            }, function (response) {
                if (response.result) {
                    heading.find("span").html(stateName);
                }
            }, "json");
        }).on("click", ".icon-trash",function () {
            var heading = $(this).closest(headingClass);
            $.post("/tasks/deleteState/", {
                uid: heading.attr("data-uid"),
                stateid: heading.attr("data-state-id")
            }, function (response) {
                if (response.result) {
                    heading.closest(".accordion-group").remove();
                }
            }, "json");
        }).on("click", ".accordion-group>input", function () {
            profileContainer.find(".current-state").removeClass("current-state").next(".collapse").collapse("hide");
            $(this).next(".accordion-heading").addClass("current-state").next(".collapse").collapse("show");
        });
    $("#addState").click(function () {
        $('<div class="accordion-group"></div>').prependTo(profileContainer).load("/tasks/addState/", function () {
            $(this).find(".icon-pencil").click();
        });
    });
});