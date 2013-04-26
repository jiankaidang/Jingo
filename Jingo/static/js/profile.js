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
    }).on("blur", "input", function () {
            var heading = $(this).closest(headingClass);
            heading.find("a").show();
            var stateNameInput = heading.find("input").hide();
            new CsrfAuth().ajaxRequest("/tasks/updateState/", {
                data: {
                    uid: profileContainer.attr("data-uid"),
                    stateid: heading.attr("data-state-id"),
                    state_name: stateNameInput.val()
                },
                'success': function (response) {
                    if (response.result) {
                        alert("the user name is '" + response.data + "'");
                    } else
                        alert('can\'t find this user!');
                },
                'error': function (xhr, textStatus, thrownError) {
                    alert(xhr.statusText);
                    alert(xhr.responseText);
                }
            });
        });
});