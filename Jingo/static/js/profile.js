/**
 * Author: Jiankai Dang
 * Date: 4/25/13
 * Time: 11:49 PM
 */
$(function () {
    var headingClass = ".accordion-heading";
    $("#accordion2").on("click", ".icon-pencil",function () {
        var heading = $(this).closest(headingClass);
        heading.find("a").hide();
        heading.find("input").show().focus();
    }).on("blur", "input",function () {
            var heading = $(this).closest(headingClass);
            heading.find("a").show();
            var stateNameInput = heading.find("input:text").hide(), stateName = stateNameInput.val();
            new CsrfAuth().ajaxRequest("/tasks/updateState/", {
                data: {
                    uid: heading.attr("data-uid"),
                    stateid: heading.attr("data-state-id"),
                    state_name: stateName
                },
                'success': function (response) {
                    if (response.result) {
                        heading.find("span").html(stateName);
                    } else
                        alert('error');
                },
                'error': function (xhr, textStatus, thrownError) {
                    alert(xhr.statusText);
                    alert(xhr.responseText);
                }
            });
        }).on("click", ".icon-trash", function () {
        	var heading = $(this).closest(headingClass);
            new CsrfAuth().ajaxRequest("/tasks/deleteState/", {
                data: {
                    uid: heading.attr("data-uid"),
                    stateid: heading.attr("data-state-id")
                },
                'success': function (response) {
                    if (response.result) {
                        $(this).closest(".accordion-group").remove();
                    } else
                        alert('error');
                },
                'error': function (xhr, textStatus, thrownError) {
                    alert(xhr.statusText);
                    alert(xhr.responseText);
                }
            });
        });
});