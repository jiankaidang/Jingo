/**
 * Author: Jiankai Dang
 * Date: 5/5/13
 * Time: 2:36 PM
 */
$(function () {
    var container = $("#accordion2"), uid = container.attr("data-uid");
    container.on("click", ".unfollow-friend",function () {
        $.post("/tasks/unfollow/", {
            uid: uid,
            f_uid: $(this).attr("f_uid")
        }, function () {
            location.reload();
        });
    }).on("click", ".accept-friend",function () {
            $.post("/tasks/replyInvitation/", {
                invitationid: $(this).closest("li").attr("invitationid"),
                reply: 1
            }, function () {
                location.reload();
            });
        }).on("click", ".deny-friend", function () {
            $.post("/tasks/replyInvitation/", {
                invitationid: $(this).closest("li").attr("invitationid"),
                reply: 0
            }, function () {
                location.reload();
            });
        });
});