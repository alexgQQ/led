const width = 32;
const height = 8;
const off_color = '#000000';
const on_color = '#FFFFFF';

var data = [];
for (var i = 0; i < height; i++) {
  data[i] = [];
  for (var e = 0; e < width; e++) {
    data[i][e] = [0, 0, 0]
  }
}

$(document).ready(function() {
  $("table").click();
});

$(".off").click(function() {
  $(".select").removeClass("select");
  $("table").click();
});

$(".on").click(function() {
  $("td").addClass("select");
  $("table").click();
});

$(".invert").click(function() {
  $("td").toggleClass("select");
  $("table").click();
});

$("td").click(function() {
  if ($(this).hasClass("select")) {
    $(this).removeClass("select");
  } else {
    $(this).addClass("select");
  }
});

$("table").click(function() {
  var table = $("table").first();
  var cols = table.find("tr");
  cols.each(function() {
    var rows = $(this).find("td");
    rows.each(function() {
      console.log($(this).parent().data("row"), $(this).data("col"))
      data[$(this).parent().data("row")][$(this).data("col")] = $(this).hasClass(
        "select"
      )
        ? 1
        : 0;
    });
  });
  array = convert();
  postData(`http://192.168.0.16/board`, {"data": array})
    .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
    .catch(error => console.error(error));
});

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
  } : null;
}

function convert() {
  var buffer = [];
  for (var i = 0; i < height; i++) {
    buffer[i] = [];
    for (var j = 0; j < width; j++) {
      if (data[i][e] == 1) {
        buffer[i][e] = hexToRgb(on_color);
      } else {
        buffer[i][e] = hexToRgb(off_color);
      }
    }
  }
  
  return buffer
}

function postData(url = ``, data = {}) {
  // Default options are marked with *
    return fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(response => response.json()); // parses JSON response into native Javascript objects 
};
