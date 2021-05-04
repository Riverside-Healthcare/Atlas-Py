(function (d, a) {
  "object" === typeof exports
    ? (module.exports = a(window, document))
    : (d.SimpleScrollbar = a(window, document));
})(this, function (d, a) {
  function f(b) {
    new g(b);
    /*Object.prototype.hasOwnProperty.call(b, "data-simple-scrollbar") || Object.defineProperty(b, "data-simple-scrollbar", {
            value: new g(b)
        })*/
  }

  function m(b, c) {
    function h(b) {
      var a = b.pageY - e;
      e = b.pageY;
      k(function () {
        c.el.scrollTop += a / c.scrollRatio;
      });
    }

    function d() {
      c.target.classList.remove("ss-grabbed");
      b.classList.remove("ss-grabbed");
      a.body.classList.remove("ss-grabbed");
      a.removeEventListener("mousemove", h);
      a.removeEventListener("mouseup", d);
    }
    var e;
    b.addEventListener("mousedown", function (g) {
      e = g.pageY;
      c.target.classList.add("ss-grabbed");
      b.classList.add("ss-grabbed");
      a.body.classList.add("ss-grabbed");
      a.addEventListener("mousemove", h);
      a.addEventListener("mouseup", d);
      return !1;
    });
  }
  function q(b, c) {
    function h(b) {
      var a = b.pageX - e;
      e = b.pageX;
      k(function () {
        c.el.scrollLeft += a / c.scrollRatioH;
      });
    }

    function d() {
      c.target.classList.remove("ss-grabbed");
      b.classList.remove("ss-grabbed");
      a.body.classList.remove("ss-grabbed");
      a.removeEventListener("mousemove", h);
      a.removeEventListener("mouseup", d);
    }
    var e;
    b.addEventListener("mousedown", function (g) {
      e = g.pageX;
      c.target.classList.add("ss-grabbed");
      b.classList.add("ss-grabbed");
      a.body.classList.add("ss-grabbed");
      a.addEventListener("mousemove", h);
      a.addEventListener("mouseup", d);
      return !1;
    });
  }

  function mp(b, c) {
    function h(b) {
      var a = b.pageY - e;
      e = b.pageY;
      k(function () {
        c.el.scrollTop += a / c.scrollRatioP;
      });
    }

    function d() {
      c.target.classList.remove("ss-grabbed");
      b.classList.remove("sp-grabbed");
      a.body.classList.remove("sp-grabbed");
      a.removeEventListener("mousemove", h);
      a.removeEventListener("mouseup", d);
    }
    var e;
    c.pwrapper.addEventListener(
      "mousewheel",
      function (l) {
        l.preventDefault();
        c.el.scrollTop += l.deltaY;
      },
      { passive: true }
    );
    c.pwrapper.addEventListener("click", function (l) {
      l = window.event || l;
      if (l.target != c.pbar) {
        c.el.scrollTop =
          (l.clientY -
            c.pwrapper.getBoundingClientRect().top -
            (c.el.clientHeight / 2) * c.scrollRatioP) /
          c.scrollRatioP;
      }
    });
    b.addEventListener("mousedown", function (g) {
      e = g.pageY;
      c.target.classList.add("ss-grabbed");
      b.classList.add("sp-grabbed");
      a.body.classList.add("sp-grabbed");
      a.addEventListener("mousemove", h);
      a.addEventListener("mouseup", d);
      return !1;
    });
  }

  function e(b) {
    this.target = b;
    // set height of parent
    if (b.parentElement.classList.contains("query-box"))
      b.parentElement.style.height =
        Math.min(b.parentElement.clientHeight + 50, 500) + "px";
    this.bar = '<div class="ss-scroll"><div class="ss-liner">';
    this.hbar = '<div class="ss-hscroll"><div class="ss-liner">';
    this.wrapper = a.createElement("div");
    this.wrapper.setAttribute("class", "ss-wrapper");
    this.el = a.createElement("div");
    this.el.setAttribute("class", "ss-content");
    for (this.wrapper.appendChild(this.el); this.target.firstChild; )
      this.el.appendChild(this.target.firstChild);
    this.target.appendChild(this.wrapper);
    this.wrapper.insertAdjacentHTML("beforeend", this.bar);
    this.bar = this.wrapper.lastChild;
    this.wrapper.insertAdjacentHTML("beforeend", this.hbar);
    this.hbar = this.wrapper.lastChild;
    m(this.bar, this);
    q(this.hbar, this);
    this.moveBar();
    this.moveHBar();
    //d.addEventListener("resize", this.moveBar.bind(this));
    this.el.addEventListener("scroll", this.moveBar.bind(this));
    this.el.addEventListener("input", this.moveBar.bind(this));
    this.el.addEventListener("mouseenter", this.moveBar.bind(this));

    //d.addEventListener("resize", this.moveHBar.bind(this));
    this.el.addEventListener("scroll", this.moveHBar.bind(this));
    this.el.addEventListener("input", this.moveHBar.bind(this));
    this.el.addEventListener("mouseenter", this.moveHBar.bind(this));

    this.target.classList.add("ss-container");

    var c = d.getComputedStyle(b);
    "0px" === c.height &&
      "0px" !== c["max-height"] &&
      (b.style.height = c["max-height"]);

    /* preview scroll */
    if (this.target.classList.contains("ss-preview")) {
      this.pbar = '<div class="sp-scroll">';
      this.pwrapper = a.createElement("div");
      this.pwrapper.setAttribute("class", "sp-wrapper");
      this.pcontent = a.createElement("div");
      this.pcontent.setAttribute("class", "sp-content");
      // get existing content reference
      this.pcontent.innerHTML = this.el.cloneNode(true).innerHTML;
      this.pwrapper.appendChild(this.pcontent);
      this.wrapper.appendChild(this.pwrapper);
      this.pwrapper.insertAdjacentHTML("beforeend", this.pbar);
      this.pbar = this.pwrapper.lastChild;
      mp(this.pbar, this);
      this.updatePreview();
      //d.addEventListener("resize", this.updatePreview.bind(this));
      this.el.addEventListener("scroll", this.updatePreview.bind(this));
      this.el.addEventListener("input", this.updatePreview.bind(this));
      this.el.addEventListener("mouseenter", this.updatePreview.bind(this));
      this.target.classList.add("sp-container");
    }
  }

  function l() {
    for (
      var b = a.querySelectorAll("*[ss-container]:not(.ss-container)"), c = 0;
      c < b.length;
      c++
    )
      f(b[c]);
  }
  var k =
    d.requestAnimationFrame ||
    d.setImmediate ||
    function (b) {
      return setTimeout(b, 0);
    };
  e.prototype = {
    moveBar: function (b) {
      var c = this.el.scrollHeight,
        a = this;
      this.scrollRatio = this.el.clientHeight / c;
      k(function () {
        1 <= a.scrollRatio
          ? a.bar.classList.add("ss-hidden")
          : (a.bar.classList.remove("ss-hidden"),
            (a.bar.style.cssText =
              "height:" +
              Math.max(100 * a.scrollRatio, 10) +
              "%; top:" +
              Math.min((a.el.scrollTop / c) * 100, 90) +
              "%;"));
      });
    },
    moveHBar: function (b) {
      var c = this.el.scrollWidth,
        a = this;
      this.scrollRatioH = this.el.clientWidth / c;
      k(function () {
        1 <= a.scrollRatioH
          ? a.hbar.classList.add("ss-hidden")
          : (a.hbar.classList.remove("ss-hidden"),
            (a.hbar.style.cssText =
              "width:" +
              Math.max(100 * a.scrollRatioH, 10) +
              "%; left:" +
              Math.min((a.el.scrollLeft / c) * 100, 90) +
              "%;"));
      });
    },
    updatePreview: function (b) {
      var a = this,
        p = this.pcontent.getElementsByTagName("pre")[0];
      this.transformX = Math.min(130 / p.clientWidth); //,a.el.clientHeight/p.clientHeight);
      this.scrollRatioP = Math.min(
        this.transformX,
        a.el.clientHeight / p.clientHeight
      );

      k(function () {
        a.pcontent.style.transform =
          "scale(0" + a.transformX + ", 0" + a.scrollRatioP + ")";
        a.pwrapper.style.width = Math.min(130, a.el.clientWidth * 0.15) + "px";
        a.pbar.style.cssText =
          "height:" +
          a.el.clientHeight * a.scrollRatioP +
          "px; top:" +
          a.el.scrollTop * a.scrollRatioP +
          "px;";
      });
    },
  };
  a.addEventListener("DOMContentLoaded", l);
  a.addEventListener("ajax", l);
  a.addEventListener("ss-load", function (e) {
    if (typeof e.detail !== "undefined" && !!e.detail && !!e.detail.el) {
      f(e.detail.el);
    } else {
      l();
    }
  });

  e.initEl = f;
  e.initAll = l;
  var g = e;
  return g;
});

SimpleScrollbar.initAll();
