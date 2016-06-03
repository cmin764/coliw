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
        H.pop();
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
    h.text(h.text() + EOL + text);
    h.scrollTop(h.scrollTop() + h.height());
}


function disable_cli() {
    $("#cli-entry").prop("disabled", true);
}


function enable_cli() {
    $("#cli-entry").prop("disabled", false);
}


function show_alert(msg, ok) {
    var content = `
        <div class="alert alert-{0} text-center" role="alert">
            {1}
        </div>
    `;
    var alert = ok ? "success" : "danger";
    content = String.format(content, alert, msg);
    var s = $("#alert");
    s.empty();
    s.append(content);
}


function handle_response(code, response) {
    if (!code) {
        show_alert("Success", true);
    } else {
        var msg = ERROR[code] + " (" + code + ")";
        show_alert(msg, false);
    }
    save_history(response);
}


function loadall() {
    // Clear everything under the terminal history.
    $("#clear").click(function () {
        $("#cli-history").text("");
    });

    // Send commands to the server and show output.
    $("#cli-entry").keypress(function (event) {
        var key = event.keyCode;

        if (key == 13) {
            // Enter.
            var cmd = $(this).val();
            $(this).val("");
            if (!cmd) {
                return;    // empty command
            }
            save_cmd(cmd);
            // Show it into the history.
            save_history(cmd);
            // Send string through API.
            disable_cli();
            var req = $.ajax({
                method: "POST",
                url: "/command",
                data: {cmd: cmd},
            });
            req.done(function (resp) {
                enable_cli();
                handle_response(resp["code"], resp["response"]);
            });
            req.fail(function () {
                enable_cli();
                show_alert("Invalid command", false);
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
}


$(document).ready(loadall);
