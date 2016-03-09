d3.select("body")
  .append("svg")
  .attr("width", 50)
  .attr("height", 50)
  .append("circle")
  .attr("cx", 25)
  .attr("cy", 25)
  .attr("r", 25)
  .style("fill", "purple");


var bodySelection = d3.select("body");
 
var svgSelection = bodySelection.append("svg")
      .attr("width", 50)
      .attr("height", 50);

var circleSelection = svgSelection.append("circle")
      .attr("cx", 25)
      .attr("cy", 25)
      .attr("r", 25)
      .style("fill", "purple");

var theData = [ 1, 2, 3 ]

var p = d3.select("body").selectAll("p")
  .data(theData)
  .enter()
  .append("p")
  .text(function (d,i) {
  	return "i = " + i + " d = "+d;
  });

console.log(p);



var jsonCircles = [
  {
   "x_axis": 30,
   "y_axis": 30,
   "radius": 20,
   "color" : "green"
  }, {
   "x_axis": 70,
   "y_axis": 70,
   "radius": 20,
   "color" : "purple"
  }, {
   "x_axis": 110,
   "y_axis": 100,
   "radius": 20,
   "color" : "red"
}];

//var spaceCircles = [30, 70, 110];

var svgContainer = d3.select("body").append("svg")
                                    .attr("width", 200)
                                    .attr("height", 200);
                                    //.style("border", "1px solid black");

var circles = svgContainer.selectAll("circle")
	                      .data(jsonCircles)
                          .enter()
                          .append("circle");                                 

var circleAttributes = circles
                       .attr("cx", function (d) { return d.x_axis; })
                       .attr("cy", function (d) { return d.y_axis; })
                       .attr("r", function (d) { return d.radius; })
                       .style("fill", function (d) { return d.color; });
                        // var returnColor;
                        //if (d === 30) { returnColor = "green";
                        // } else if (d === 70) { returnColor = "purple";
                        // } else if (d === 110) { returnColor = "red"; }
                        // return returnColor;
                       //});

var line = svgContainer.append("line")
                         .attr("x1", 5)
                         .attr("y1", 5)
                         .attr("x2", 50)
                         .attr("y2", 50)
                         .attr("stroke-width", 2)
                         .attr("stroke", "black");




//The data for our line
var lineData = [ { "x": 1,   "y": 5},  { "x": 20,  "y": 20},
                 { "x": 40,  "y": 10}, { "x": 60,  "y": 40},
                 { "x": 80,  "y": 5},  { "x": 100, "y": 60}];

//This an accessor function
var lineFunction = d3.svg.line()
                   .x(function(d) { return d.x; })
                   .y(function(d) { return d.y; })
                   .interpolate("linear");

//The SVG Container
var svgContainer = d3.select("body").append("svg")
                                    .attr("width", 200)
                                    .attr("height", 200);

//The line SVG Path we draw
var lineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");




//scale SVG coordinate space to include the data
var jsonRectangles = [
  { "x_axis": 10, "y_axis": 10, "height": 20, "width":20, "color" : "green" },
  { "x_axis": 40, "y_axis": 40, "height": 20, "width":20, "color" : "purple" },
  { "x_axis": 70, "y_axis": 70, "height": 20, "width":20, "color" : "red" }];

var max_x = 0;
var max_y = 0;
//We loop through our jsonRectangles array
for (var i = 0; i < jsonRectangles.length; i++) {
  var temp_x, temp_y;
  // To get the farthest right hand point, we need to add the x-coordinate and the width
  var temp_x = jsonRectangles[i].x_axis + jsonRectangles[i].width;
  // To get the farthest bottom point, we need to add the y-coordinate and the height
  var temp_y = jsonRectangles[i].y_axis + jsonRectangles[i].height;

  if ( temp_x >= max_x ) {
    max_x = temp_x;
  }
  if ( temp_y >= max_y ) {
    max_y = temp_y;
  }
}

var svgContainer = d3.select("body").append("svg")
                                    .attr("width", max_x + 20)
                                    .attr("height", max_y + 20);

var rectangles = svgContainer.selectAll("rect")
                             .data(jsonRectangles)
                             .enter()
                             .append("rect");

var rectangleAttributes = rectangles
                          .attr("x", function (d) { return d.x_axis; })
                          .attr("y", function (d) { return d.y_axis; })
                          .attr("height", function (d) { return d.height; })
                          .attr("width", function (d) { return d.width; })
                          .style("fill", function(d) { return d.color; });


//can't keep scaling coordinate space upwards to encompass data
//it can quickly become larger than our browser window
//We will instead scale our data to fit into the space alloted
//scales provides functions to perform data transformations - map an input domain to out range

var initialScaleData = [0, 1000, 3000, 2000, 5000, 4000, 7000, 6000, 9000, 8000, 10000];
var newScaledData = [];
var minDataPoint = d3.min(initialScaleData);
var maxDataPoint = d3.max(initialScaleData);

//default domain, range scale is [0,1]
var linearScale = d3.scale.linear()
                   .domain([minDataPoint,maxDataPoint])
                   .range([0,100]);

for (var i = 0; i < initialScaleData.length; i++) {
  newScaledData[i] = linearScale(initialScaleData[i]);
}







//SVG groups

var circleData = [
  { "cx": 20, "cy": 20, "radius": 20, "color" : "green" },
  { "cx": 70, "cy": 70, "radius": 20, "color" : "purple" }];


var rectangleData = [
  { "rx": 110, "ry": 110, "height": 30, "width": 30, "color" : "blue" },
  { "rx": 160, "ry": 160, "height": 30, "width": 30, "color" : "red" }];

var svgContainer = d3.select("body").append("svg")
                                     .attr("width",1000)
                                     .attr("height",1000);
//Add a group to hold the circles
var circleGroup = svgContainer.append("g")
							  .attr("transform", "translate(500,500)");

//Add circles to the circleGroup
var circles = circleGroup.selectAll("circle")
                          .data(circleData)
                          .enter()
                          .append("circle");

var circleAttributes = circles
                       .attr("cx", function (d) { return d.cx; })
                       .attr("cy", function (d) { return d.cy; })
                       .attr("r", function (d) { return d.radius; })
                       .style("fill", function (d) { return d.color; });

// * Note * that the rectangles are added to the svgContainer, not the circleGroup
var rectangles = svgContainer.selectAll("rect")
                              .data(rectangleData)
                              .enter()
                              .append("rect");

var rectangleAttributes = rectangles
                          .attr("x", function (d) { return d.rx; })
                          .attr("y", function (d) { return d.ry; })
                          .attr("height", function (d) { return d.height; })
                          .attr("width", function (d) { return d.width; })
                          .style("fill", function(d) { return d.color; });






//Circle Data Set
var circleData = [
  { "cx": 20, "cy": 20, "radius": 20, "color" : "green" },
  { "cx": 70, "cy": 70, "radius": 20, "color" : "purple" }];

//Create the SVG Viewport
var svgContainer = d3.select("body").append("svg")
                                     .attr("width",200)
                                     .attr("height",200);

//Add circles to the svgContainer
var circles = svgContainer.selectAll("circle")
                           .data(circleData)
                           .enter()
                           .append("circle");

//add the circle attributes
var circleAttributes = circles
                       .attr("cx", function (d) { return d.cx; })
                       .attr("cy", function (d) { return d.cy; })
                       .attr("r", function (d) { return d.radius; })
                       .style("fill", function (d) { return d.color; });                           

//Add the SVG Text Element to the svgContainer
var text = svgContainer.selectAll("text")
                        .data(circleData)
                        .enter()
                        .append("text");

//Add SVG Text Element Attributes
var textLabels = text
                 .attr("x", function(d) { return d.cx; })
                 .attr("y", function(d) { return d.cy; })
                 //text coordiantes
                 .text( function (d) { return "( " + d.cx + ", " + d.cy +" )"; })
                 .attr("font-family", "sans-serif")
                 .attr("font-size", "20px")
                 .attr("fill", "red");






//Create the SVG Viewport
var svgContainer = d3.select("body").append("svg")
                                    .attr("width", 400)
                                    .attr("height", 100);

//Create the Scale we will use for the Axis
var axisScale = d3.scale.linear()
                        .domain([0, 100])
                        .range([0, 400]);
//Create the Axis
var xAxis = d3.svg.axis()
                  .scale(axisScale);


//Create an SVG group Element for the Axis elements and call the xAxis function
var xAxisGroup = svgContainer.append("g")
                             .call(xAxis);

