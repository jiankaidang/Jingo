/**
 * Author: Jiankai Dang
 * Date: 4/25/13
 * Time: 11:49 PM
 */
$(function () {
    var headingClass = ".accordion-heading";
    $(headingClass).on("click", ".icon-pencil",function () {
        var heading = $(this).closest(headingClass);
        heading.find("a").hide();
        heading.find("input").show().focus();
    }).on("blur", "input", function () {
            var heading = $(this).closest(headingClass);
            heading.find("a").show();
            heading.find("input").hide();
        });
});