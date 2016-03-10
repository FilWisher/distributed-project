(function() {
    var e, t;
    e = typeof exports != "undefined" && exports !== null ? exports : this, e.expander = (t = e.expander) != null ? t : {}, e.expander.network = function(e, t, n, r) {
        var i, s, o, u, a, f, l, c, h, p, d, v, m, g, y, b, w, E, S, x, T, N, C, k;
        o = {
            where: "#chart",
            width: 800,
            height: 600,
            charge: - 120,
            linkDistance: 30,
            nodeOpacity: .8,
            linkOpacity: .45,
            fadedOpacity: .1,
            mousedOverNodeOpacity: .9,
            mousedOverLinkOpacity: .9,
            nodeStrokeWidth: 1.5,
            nodeStrokeColor: "black",
            colorField: "personalized_pagerank",
            startingColor: "#FFFFD9",
            endingColor: "#BD0026"
        }, r = $.extend({}, o, r), i = function() {
            var t, i, s;
            s = [];
            for (t = 0, i = e.length; t < i; t++)
                T = e[t], T.name !== n && s.push(T[r.colorField]);
            return s
        }(), s = d3.scale.linear().domain([d3.min(i), d3.max(i)]).range([r.startingColor, r.endingColor]), b = d3.scale.linear().domain([1, 4]).range([1, 4]), y = function(e) {
            return Math.pow(b(e.level + .5), 1.8)
        }, E = d3.select(r.where).append("svg").attr("width", r.width).attr("height", r.height), a = d3.layout.force().charge(r.charge).linkDistance(r.linkDistance).size([r.width, r.height]).nodes(e).links(t).start(), d = E.selectAll("line.link").data(a.links()).enter().append("line").attr("class", "link").attr("opacity", r.linkOpacity), p = {}, k = a.links();
        for (N = 0, C = k.length; N < C; N++)
            h = k[N], p[h.source.index + "," + h.target.index] = 1;
        return f = function(e, t) {
            return p[e.index + "," + t.index] || p[t.index + "," + e.index] || e.index === t.index
        }, c = function(e, t) {
            return p[e.index + "," + t.index]
        }, l = function(e, t) {
            return p[t.index + "," + e.index]
        }, u = function(e) {
            return v.style("opacity", function(t) {
                return f(e, t) ? r.mousedOverNodeOpacity : r.fadedOpacity
            }), v.style("fill", function(t) {
                var n;
                return n = c(e, t) && l(e, t) ? "#7570B3" : c(e, t) ? "#1B9E77" : c(t, e) ? "#D95F02" : "black", this.setAttribute("fill", n), n
            }), d.style("opacity", function(t) {
                return t.source === e || t.target === e ? r.mousedOverLinkOpacity : r.fadedOpacity
            })
        }, m = function() {
            return v.style("fill", function(e) {
                return s(e[r.colorField])
            }).style("stroke", r.nodeStrokeColor).style("stroke-width", r.nodeStrokeWidth).call(a.drag).style("opacity", r.nodeOpacity), w.style("fill", "black"), a.nodes(a.nodes()).links(a.links()).start()
        }, S = function() {
            return v.style("fill", function(e) {
                return s(e[r.colorField])
            }).call(a.drag).style("opacity", r.nodeOpacity), w.style("fill", "black"), d.style("opacity", r.linkOpacity)
        }, v = E.selectAll("circle.node").data(a.nodes()).enter().append("circle").attr("class", "node").attr("r", function(e) {
            return y(e)
        }).call(a.drag).on("mouseover", function(e) {
            return u(e)
        }).on("mouseout", function(e) {
            return S()
        }), w = v.filter(function(e) {
            return e.name === n
        }), m(), a.on("tick", function() {
            return d.attr("x1", function(e) {
                return e.source.x
            }).attr("y1", function(e) {
                return e.source.y
            }).attr("x2", function(e) {
                return e.target.x
            }).attr("y2", function(e) {
                return e.target.y
            }), v.attr("cx", function(e) {
                return e.x
            }).attr("cy", function(e) {
                return e.y
            })
        }), x = function(t) {
            var o;
            return r.colorField = t, i = function() {
                var t, i, s;
                s = [];
                for (t = 0, i = e.length; t < i; t++)
                    o = e[t], o.name !== n && s.push(o[r.colorField]);
                return s
            }(), s = d3.scale.linear().domain([d3.min(i), d3.max(i)]).range([r.startingColor, r.endingColor]), E.selectAll("circle.node").data(a.nodes()).filter(function(e) {
                return e.name !== n
            }).transition().duration(1e3).style("fill", function(e) {
                return s(e[r.colorField])
            })
        }, g = {}, g.links = d, g.nodes = v, g.updateColor = x, g
    }
}).call(this);

