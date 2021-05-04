/*
    Atlas of Information Management business intelligence library and documentation database.
    Copyright (C) 2020  Riverside Healthcare, Kankakee, IL

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

// only if IE
// https://stackoverflow.com/a/21712356/10265880
if (window.document.documentMode) {
  function _instanceof(left, right) {
    if (
      right != null &&
      typeof Symbol !== "undefined" &&
      right[Symbol.hasInstance]
    ) {
      return !!right[Symbol.hasInstance](left);
    } else {
      return left instanceof right;
    }
  }

  Element.prototype.matches ||
    (Element.prototype.matches =
      Element.prototype.msMatchesSelector ||
      Element.prototype.webkitMatchesSelector),
    Element.prototype.closest ||
      (Element.prototype.closest = function (t) {
        var e = this;

        do {
          if (e.matches(t)) return e;
          e = e.parentElement || e.parentNode;
        } while (null !== e && 1 === e.nodeType);

        return null;
      }),
    (function () {
      function t(t, e) {
        e = e || {
          bubbles: !1,
          cancelable: !1,
          detail: void 0,
        };
        var n = document.createEvent("CustomEvent");
        return n.initCustomEvent(t, e.bubbles, e.cancelable, e.detail), n;
      }

      if ("function" != typeof window.CustomEvent) {
        t.prototype = window.Event.prototype;
        window.CustomEvent = t;
      }
    })(),
    String.prototype.startsWith ||
      (Object.defineProperty(String.prototype, "startsWith", {
        value: function value(t, e) {
          var n = e > 0 ? 0 | e : 0;
          return this.substring(n, n + t.length) === t;
        },
      }),
      Array.from ||
        (Array.from = (function () {
          var t = Object.prototype.toString,
            e = function e(_e) {
              return (
                "function" == typeof _e || "[object Function]" === t.call(_e)
              );
            },
            n = Math.pow(2, 53) - 1,
            r = function r(t) {
              var e = (function (t) {
                var e = Number(t);
                return isNaN(e)
                  ? 0
                  : 0 !== e && isFinite(e)
                  ? (e > 0 ? 1 : -1) * Math.floor(Math.abs(e))
                  : e;
              })(t);

              return Math.min(Math.max(e, 0), n);
            };

          return function (t) {
            var n = Object(t);
            if (null == t)
              throw new TypeError(
                "Array.from requires an array-like object - not null or undefined"
              );
            var o,
              a = arguments.length > 1 ? arguments[1] : void 0;

            if (void 0 !== a) {
              if (!e(a))
                throw new TypeError(
                  "Array.from: when provided, the second argument must be a function"
                );
              if (arguments.length > 2) o = arguments[2];
            }

            for (
              var i,
                c = r(n.length),
                u = e(this) ? Object(new this(c)) : new Array(c),
                l = 0;
              l < c;

            ) {
              (i = n[l]),
                (u[l] = a ? (void 0 === o ? a(i, l) : a.call(o, i, l)) : i),
                (l += 1);
            }

            return (u.length = c), u;
          };
        })()),
      [
        Element.prototype,
        Document.prototype,
        DocumentFragment.prototype,
      ].forEach(function (t) {
        t.hasOwnProperty("append") ||
          Object.defineProperty(t, "append", {
            configurable: !0,
            enumerable: !0,
            writable: !0,
            value: function value() {
              var t = Array.prototype.slice.call(arguments),
                e = document.createDocumentFragment();
              t.forEach(function (t) {
                var n = _instanceof(t, Node);

                e.appendChild(n ? t : document.createTextNode(String(t)));
              }),
                this.appendChild(e);
            },
          });
      }));

  /*! (c) Andrea Giammarchi - ISC */
  var self = this || {};
  try {
    self.EventTarget = new EventTarget().constructor;
  } catch (e) {
    !(function (e, o) {
      var t = e.create,
        r = e.defineProperty,
        n = i.prototype;

      function i() {
        "use strict";
        o.set(this, t(null));
      }

      function s(e, t, n) {
        r(e, t, {
          configurable: !0,
          writable: !0,
          value: n,
        });
      }

      function a(e) {
        var t = e.options;
        t && t.once && e.target.removeEventListener(this.type, e.listener),
          "function" == typeof e.listener
            ? e.listener.call(e.target, this)
            : e.listener.handleEvent(this);
      }
      s(n, "addEventListener", function (e, t, n) {
        for (
          var r = o.get(this), i = r[e] || (r[e] = []), s = 0, a = i.length;
          s < a;
          s++
        )
          if (i[s].listener === t) return;
        i.push({
          target: this,
          listener: t,
          options: n,
        });
      }),
        s(n, "dispatchEvent", function (e) {
          var t = o.get(this)[e.type];
          return (
            t &&
              (s(e, "target", this),
              s(e, "currentTarget", this),
              t.slice(0).forEach(a, e),
              delete e.currentTarget,
              delete e.target),
            !0
          );
        }),
        s(n, "removeEventListener", function (e, t) {
          for (
            var n = o.get(this), r = n[e] || (n[e] = []), i = 0, s = r.length;
            i < s;
            i++
          )
            if (r[i].listener === t) return void r.splice(i, 1);
        }),
        (self.EventTarget = i);
    })(Object, new WeakMap());
  }

  (function () {
    var supportsPassive = false;
    document.createElement("div").addEventListener("test", function () {}, {
      get passive() {
        supportsPassive = true;
        return false;
      },
    });

    if (!supportsPassive) {
      var super_add_event_listener = EventTarget.prototype.addEventListener;
      var super_remove_event_listener =
        EventTarget.prototype.removeEventListener;
      var super_prevent_default = Event.prototype.preventDefault;

      function parseOptions(type, listener, options, action) {
        var needsWrapping = false;
        var useCapture = false;
        var passive = false;
        var fieldId;
        if (options) {
          if (typeof options === "object") {
            passive = options.passive ? true : false;
            useCapture = options.useCapture ? true : false;
          } else {
            useCapture = options;
          }
        }
        if (passive) needsWrapping = true;
        if (needsWrapping) {
          fieldId = useCapture.toString();
          fieldId += passive.toString();
        }
        action(needsWrapping, fieldId, useCapture, passive);
      }

      Event.prototype.preventDefault = function () {
        if (this.__passive) {
          console.warn(
            "Ignored attempt to preventDefault an event from a passive listener"
          );
          return;
        }
        super_prevent_default.apply(this);
      };

      EventTarget.prototype.addEventListener = function (
        type,
        listener,
        options
      ) {
        var super_this = this;
        parseOptions(
          type,
          listener,
          options,
          function (needsWrapping, fieldId, useCapture, passive) {
            if (needsWrapping) {
              var fieldId = useCapture.toString();
              fieldId += passive.toString();

              if (!this.__event_listeners_options)
                this.__event_listeners_options = {};
              if (!this.__event_listeners_options[type])
                this.__event_listeners_options[type] = {};
              if (!this.__event_listeners_options[type][listener])
                this.__event_listeners_options[type][listener] = [];
              if (this.__event_listeners_options[type][listener][fieldId])
                return;
              var wrapped = {
                handleEvent: function (e) {
                  e.__passive = passive;
                  if (typeof listener === "function") {
                    listener(e);
                  } else {
                    listener.handleEvent(e);
                  }
                  e.__passive = false;
                },
              };
              this.__event_listeners_options[type][listener][fieldId] = wrapped;
              super_add_event_listener.call(
                super_this,
                type,
                wrapped,
                useCapture
              );
            } else {
              super_add_event_listener.call(
                super_this,
                type,
                listener,
                useCapture
              );
            }
          }
        );
      };

      EventTarget.prototype.removeEventListener = function (
        type,
        listener,
        options
      ) {
        var super_this = this;
        parseOptions(
          type,
          listener,
          options,
          function (needsWrapping, fieldId, useCapture, passive) {
            if (
              needsWrapping &&
              this.__event_listeners_options &&
              this.__event_listeners_options[type] &&
              this.__event_listeners_options[type][listener] &&
              this.__event_listeners_options[type][listener][fieldId]
            ) {
              super_remove_event_listener.call(
                super_this,
                type,
                this.__event_listeners_options[type][listener][fieldId],
                false
              );
              delete this.__event_listeners_options[type][listener][fieldId];
              if (this.__event_listeners_options[type][listener].length == 0)
                delete this.__event_listeners_options[type][listener];
            } else {
              super_remove_event_listener.call(
                super_this,
                type,
                listener,
                useCapture
              );
            }
          }
        );
      };
    }
  })();

  function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }
}
