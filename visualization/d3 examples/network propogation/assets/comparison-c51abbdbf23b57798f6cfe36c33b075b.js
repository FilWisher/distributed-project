(function() {
    var e, t;
    e = typeof exports != "undefined" && exports !== null ? exports : this, e.expander = (t = e.expander) != null ? t : {}, e.expander.compare = function(e, t, n, r) {
        var i, s, o, u, a, f, l, c, h, p;
        return s = {
            where: "#barchart",
            width: 800,
            height: 200,
            barWidth: 75,
            barSpacing: 4,
            colorA: "lightblue",
            colorB: "lightpink"
        }, i = function() {
            var e, r, i, s;
            i = _.zip(t, n), s = [];
            for (e = 0, r = i.length; e < r; e++)
                h = i[e], s.push(h[0] / (h[0] + h[1]));
            return s
        }(), r = $.extend({}, s, r), l = d3.select(r.where).append("svg").attr("class", "chart").attr("width", r.width + 50).attr("height", r.height + 50), p = d3.scale.linear().domain([0, 1]).range([0, r.height]), o = l.selectAll("rect.metricA").data(i).enter().append("rect").attr("x", function(e, t) {
            return t * r.barWidth
        }).attr("y", function(e) {
            return r.height - p(e)
        }).attr("width", r.barWidth - r.barSpacing).attr("height", function(e) {
            return p(e)
        }).attr("stroke", "gray").attr("stroke-width", 1).attr("stroke-opacity", .75).style("fill", r.colorA), u = l.selectAll("rect.metricB").data(i).enter().append("rect").attr("x", function(e, t) {
            return t * r.barWidth
        }).attr("y", 0).attr("width", r.barWidth - r.barSpacing).attr("height", function(e) {
            return p(1 - e)
        }).style("fill", r.colorB).attr("stroke", "gray").attr("stroke-width", 1).attr("stroke-opacity", .75), f = l.selectAll("g.rule").data([.5]).enter().append("g").attr("class", "rule").attr("transform", function(e) {
            return "translate(0," + p(e) + ")"
        }).append("line").attr("x2", r.width).style("stroke", "white").attr("stroke-width", 1).style("stroke-opacity", .25), l.selectAll("text.axis.xAxis").data(e).enter().append("svg:text").attr("x", function(e, t) {
            return t * r.barWidth
        }).attr("y", r.height).attr("dx", r.barWidth / 2).attr("text-anchor", "middle").text(function(e) {
            return e
        }).attr("transform", "translate(0, 18)").attr("fill", "gray"), l.selectAll("text.axis.yAxis").data([.5]).enter().append("svg:text").attr("x", e.length * r.barWidth).attr("y", function(e) {
            return p(e)
        }).attr("dx", 2).attr("dy", 3).attr("fill", "gray").attr("style", "font-size: 10").text("50% (MAP1 / MAP1 + MAP2)"), c = function(e, t) {
            var n;
            return i = function() {
                var r, i, s, o;
                s = _.zip(e, t), o = [];
                for (r = 0, i = s.length; r < i; r++)
                    n = s[r], o.push(n[0] / (n[0] + n[1]));
                return o
            }(), o.data(i).transition().duration(1e3).attr("y", function(e) {
                return r.height - p(e)
            }).attr("height", function(e) {
                return p(e)
            }), u.data(i).transition().duration(1e3).attr("height", function(e) {
                return p(1 - e)
            })
        }, a = {}, a.update = c, a
    }, e.expander.barchart = function(e, t, n) {
        var r, i, s, o, u, a, f;
        return r = {
            where: "#barchart",
            width: 800,
            height: 200,
            barWidth: 75,
            barSpacing: 4,
            colorA: "lightblue"
        }, n = $.extend({}, r, n), u = d3.select(n.where).append("svg").attr("class", "chart").attr("width", n.width + 50).attr("height", n.height + 50), f = d3.scale.linear().domain([0, 1]).range([0, n.height]), i = u.selectAll("rect.metricA").data(t).enter().append("rect").attr("x", function(e, t) {
            return t * n.barWidth
        }).attr("y", function(e) {
            return n.height - f(e)
        }).attr("width", n.barWidth - n.barSpacing).attr("height", function(e) {
            return f(e)
        }).attr("stroke", "gray").attr("stroke-width", 1).attr("stroke-opacity", .75).style("fill", n.colorA), o = u.selectAll("g.rule").data([.5]).enter().append("g").attr("class", "rule").attr("transform", function(e) {
            return "translate(0," + f(e) + ")"
        }).append("line").attr("x2", n.width).style("stroke", "white").attr("stroke-width", 1).style("stroke-opacity", .25), u.selectAll("text.axis.xAxis").data(e).enter().append("svg:text").attr("x", function(e, t) {
            return t * n.barWidth
        }).attr("y", n.height).attr("dx", n.barWidth / 2).attr("text-anchor", "middle").text(function(e) {
            return e
        }).attr("transform", "translate(0, 18)").attr("fill", "gray"), u.selectAll("text.axis.yAxis").data([.5]).enter().append("svg:text").attr("x", e.length * n.barWidth).attr("y", function(e) {
            return f(e)
        }).attr("dx", 2).attr("dy", 3).attr("fill", "gray").attr("style", "font-size: 10").text("0.5 (MAP)"), a = function(e) {
            return t = e, i.data(t).transition().duration(1e3).attr("y", function(e) {
                return n.height - f(e)
            }).attr("height", function(e) {
                return f(e)
            })
        }, s = {}, s.update = a, s
    }
}).call(this);

