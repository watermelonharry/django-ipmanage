/**
 * Created by water on 2017/7/24.
 */
/*
 *
 *
 *
 */
function bind_mission_terminal(js_data) {
    $.ajax({
            type: "POST",
            url: "/terminal/api/inner/bindterminal/",
            data: JSON.stringify(js_data),
            dataType: "json",
            contentType: "application/json",
            success: function (json_data) {
                console.log("success", json_data);
            },
            error: function (e) {
                console.log("failed to bind", e);
                alert("分配终端失败");
            }
        }
    )
}