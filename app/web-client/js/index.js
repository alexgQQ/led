// TODO: refacotr array usage to https://github.com/nicolaspanel/numjs


const width = 32;
const height = 8;
const off_color = '#000000';
let on_color = '#f6b73c';

var data = [];
for (var i = 0; i < width; i++) {
  data[i] = [];
  for (var e = 0; e < height; e++) {
    data[i][e] = 0
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
      data[$(this).parent().data("row")][$(this).data("col")] = $(this).hasClass(
        "select"
      )
        ? 1
        : 0;
    });
  });
  array = convert();
  const URL = 'http://192.168.0.16:5000/board'
  // const URL = 'http://127.0.0.1:5000/board'
  postData(URL, {"data": array})
    .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
    .catch(error => console.error(error));
});

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? [parseInt(result[1], 16), parseInt(result[2], 16), parseInt(result[3], 16)
 ] : null;
}

function convert() {
  var buffer = [];
  for (var i = 0; i < width; i++) {
    buffer[i] = [];
    for (var j = 0; j < height; j++) {
      if (data[i][j] == 1) {
        if (on_color.constructor === Array) {
          buffer[i][j] = on_color;
        } else {
          buffer[i][j] = hexToRgb(on_color);
        }
      } else {
        buffer[i][j] = hexToRgb(off_color);
      }
    }
  }
  return buffer
}

function postData(url, data) {
  // Default options are marked with *
    return fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "no-cors", // no-cors, cors, *same-origin
        headers: {
            "Content-Type": "application/json",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(response => response.json())
    .catch(error => console.error(error)); // parses JSON response into native Javascript objects 
};

// moduled querySelector
function qs(selectEl){
  return document.querySelector(selectEl);
}

// select RGB inputs
let red = qs('#red'), 
green = qs('#green'), 
blue = qs('#blue'); 

// selet num inputs
let redNumVal = qs('#redNum'), 
greenNumVal = qs('#greenNum'), 
blueNumVal = qs('#blueNum');

// select Color Display
let colorDisplay = qs('#color-display');

// select labels
let redLbl = qs('label[for=red]'), 
greenLbl = qs('label[for=green]'), 
blueLbl = qs('label[for=blue]');

// init display Colors
displayColors();
// init Color Vals
colorNumbrVals();
// init ColorSliderVals
initSliderColors();
// init Change Range Val
changeRangeNumVal();
// init Colors controls
colorSliders();

// display colors
function displayColors(){
  colorDisplay.style.backgroundColor = `rgb(${red.value}, ${green.value}, ${blue.value})`;
  on_color = [parseInt(red.value), parseInt(green.value), parseInt(blue.value)];
}

// initial color val when DOM is loaded 
function colorNumbrVals(){
  redNumVal.value = red.value;
  greenNumVal.value = green.value;
  blueNumVal.value = blue.value;
}

// initial colors when DOM is loaded
function initSliderColors(){
  // label bg colors
  redLbl.style.background = `rgb(${red.value},0,0)`;
  greenLbl.style.background = `rgb(0,${green.value},0)`;
  blueLbl.style.background = `rgb(0,0,${blue.value})`;

  // slider bg colors
  sliderFill(red);
  sliderFill(green);
  sliderFill(blue);
}

// Slider Fill offset
function sliderFill(clr){
  let val = (clr.value - clr.min) / (clr.max - clr.min);
  let percent = val * 100;

  // clr input
  if(clr === red){
      clr.style.background = `linear-gradient(to right, rgb(${clr.value},0,0) ${percent}%, #cccccc 0%)`;    
  } else if (clr === green) {
      clr.style.background = `linear-gradient(to right, rgb(0,${clr.value},0) ${percent}%, #cccccc 0%)`;    
  } else if (clr === blue) {
      clr.style.background = `linear-gradient(to right, rgb(0,0,${clr.value}) ${percent}%, #cccccc 0%)`;    
  }
}

// change range values by number input
function changeRangeNumVal(){

  // Validate number range
  redNumVal.addEventListener('change', ()=>{
      // make sure numbers are entered between 0 to 255
      if(redNumVal.value > 255){
          alert('cannot enter numbers greater than 255');
          redNumVal.value = red.value;
      } else if(redNumVal.value < 0) {
          alert('cannot enter numbers less than 0');  
          redNumVal.value = red.value;            
      } else if (redNumVal.value == '') {
          alert('cannot leave field empty');
          redNumVal.value = red.value;
          initSliderColors();
          displayColors();
      } else {
          red.value = redNumVal.value;
          initSliderColors();
          displayColors();
      }
  });

  // Validate number range
  greenNumVal.addEventListener('change', ()=>{
      // make sure numbers are entered between 0 to 255
      if(greenNumVal.value > 255){
          alert('cannot enter numbers greater than 255');
          greenNumVal.value = green.value;
      } else if(greenNumVal.value < 0) {
          alert('cannot enter numbers less than 0');  
          greenNumVal.value = green.value;            
      } else if(greenNumVal.value == '') {
          alert('cannot leave field empty');
          greenNumVal.value = green.value;
          initSliderColors();
          displayColors();
      } else {
          green.value = greenNumVal.value;            
          initSliderColors();
          displayColors();
      }
  });

  // Validate number range
  blueNumVal.addEventListener('change', ()=>{
      // make sure numbers are entered between 0 to 255
      if (blueNumVal.value > 255) {
          alert('cannot enter numbers greater than 255');
          blueNumVal.value = blue.value;
      } else if (blueNumVal.value < 0) {
          alert('cannot enter numbers less than 0');
          blueNumVal.value = blue.value;
      } else if(blueNumVal.value == '') {
          alert('cannot leave field empty');
          blueNumVal.value = blue.value;
          initSliderColors();
          displayColors();
      } else {
          blue.value = blueNumVal.value;            
          initSliderColors();
          displayColors();
      }
  });
}

// Color Sliders controls
function colorSliders(){
  red.addEventListener('input', () => {
      displayColors();
      initSliderColors();
      changeRangeNumVal();
      colorNumbrVals();
  });

  green.addEventListener('input', () => {
      displayColors();
      initSliderColors();
      changeRangeNumVal();
      colorNumbrVals();
  });

  blue.addEventListener('input', () => {
      displayColors();
      initSliderColors();
      changeRangeNumVal();
      colorNumbrVals();
  });
}
