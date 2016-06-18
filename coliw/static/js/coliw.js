var EOL = "\n";

var H_SIZE = 100;
var H_LIST = [];
var H_IDX = -1;

var ERROR = {
    10: "Parsing error",
    20: "Execution error",
    1: "Unknown error",
};


if (!String.format) {
  String.format = function(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}


function save_cmd(cmd) {
    H_LIST.unshift(cmd);
    if (H_LIST.length > H_SIZE) {
        H_LIST.pop();
    }
    H_IDX = -1;
}


function cmd_up() {
    H_IDX += 1;
    if (H_IDX >= H_LIST.length) {
        H_IDX = H_LIST.length - 1;
    }
    return H_LIST[H_IDX];
}


function cmd_down() {
    H_IDX -= 1;
    if (H_IDX < 0) {
        H_IDX = -1;
        return "";
    }
    return H_LIST[H_IDX];
}


function save_history(text) {
    var h = $("#cli-history");
    var cnt = h.text() + EOL + text;
    h.text(cnt.trimLeft());
    h.scrollTop(h.scrollTop() + h.height());
}


function disable_cli() {
    $("#cli-entry").prop("disabled", true);
}


function enable_cli() {
    $("#cli-entry").prop("disabled", false);
}


function show_alert(msg, type) {
    var content = `
        <div class="alert alert-{0} text-center" role="alert">
            {1}
        </div>
    `;
    content = String.format(content, type, msg);
    var s = $("#alert");
    s.empty();
    s.append(content);
}


function handle_response(code, response) {
    if (!code) {
        show_alert("Success", "success");
    } else {
        var msg = ERROR[code] + " (" + code + ")";
        show_alert(msg, "danger");
    }
    if (response) {
        save_history(response);
    }
}


function upload_history() {
    var text = $("#cli-history").text();
    var req = $.ajax({
        method: "POST",
        url: "/history",
        data: {
            h_idx: JSON.stringify(H_IDX),
            h_list: JSON.stringify(H_LIST),
            h_text: JSON.stringify(text)
        }
    });
}


function download_history() {
    var req = $.ajax({
        method: "GET",
        url: "/history"
    });
    req.done(function (resp) {
        if (!resp["status"]) {
            return;
        }
        h_idx = JSON.parse(resp["h_idx"]);
        h_list = JSON.parse(resp["h_list"]);
        h_text = JSON.parse(resp["h_text"]);
        H_IDX = h_idx;
        H_LIST = h_list;
        $("#clear").click();
        save_history(h_text);
    });
}


function loadall() {
    // Clear everything under the terminal history.
    $("#clear").click(function () {
        $("#cli-history").text("");
        $("#cli-entry").focus();
    });

    $("#autoclear").click(function () {
        var disable = $(this).prop("checked");
        $("#clear").prop("disabled", disable);
    });

    // Send commands to the server and show output.
    $("#cli-entry").keydown(function (event) {
        if (!event) {
            event = window.event;
        }
        var key = event.keyCode;
        if (event.charCode && key == 0) {
            key = event.charCode;
        }

        if (key == 13) {
            // Enter.
            var cmd = $(this).val();
            $(this).val("");
            if (!cmd) {
                return;    // empty command
            }
            if ($("#autoclear").prop("checked")) {
                $("#clear").click();
            }
            show_alert("Loading...", "warning");
            save_cmd(cmd);
            // Show it into the history.
            save_history("> " + cmd);
            // Send string through API.
            disable_cli();
            var req = $.ajax({
                method: "POST",
                url: "/command",
                data: {cmd: JSON.stringify(cmd)},
            });
            req.done(function (resp) {
                handle_response(resp["code"], resp["response"]);
                save_history(EOL);
            });
            req.fail(function () {
                show_alert("Invalid command", "danger");
            });
            req.always(function () {
                upload_history();
                enable_cli();
                $("#cli-entry").focus();
            });
        } else if (key == 38) {
            // Up arrow.
            var cmd = cmd_up();
            $(this).val(cmd);
        } else if (key == 40) {
            // Down arrow.
            var cmd = cmd_down();
            $(this).val(cmd);
        }
    });

    // Retrieve history on first load.
    download_history();
}


$(document).ready(loadall);
