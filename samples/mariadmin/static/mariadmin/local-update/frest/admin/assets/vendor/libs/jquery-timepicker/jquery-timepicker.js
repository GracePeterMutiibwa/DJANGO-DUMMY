/*! For license information please see jquery-timepicker.js.LICENSE.txt */
!(function (e, t) {
  if ('object' == typeof exports && 'object' == typeof module)
    module.exports = t(require('jQuery'));
  else if ('function' == typeof define && define.amd) define(['jQuery'], t);
  else {
    var i = 'object' == typeof exports ? t(require('jQuery')) : t(e.jQuery);
    for (var n in i) ('object' == typeof exports ? exports : e)[n] = i[n];
  }
})(self, function (e) {
  return (function () {
    var t = {
        7775: function (e, t, i) {
          var n, r, s;
          (e = i.nmd(e)),
            (function () {
              'use strict';
              function a(e) {
                return (
                  (a =
                    'function' == typeof Symbol &&
                    'symbol' == typeof Symbol.iterator
                      ? function (e) {
                          return typeof e;
                        }
                      : function (e) {
                          return e &&
                            'function' == typeof Symbol &&
                            e.constructor === Symbol &&
                            e !== Symbol.prototype
                            ? 'symbol'
                            : typeof e;
                        }),
                  a(e)
                );
              }
              function o(e, t) {
                if (!(e instanceof t))
                  throw new TypeError('Cannot call a class as a function');
              }
              function l(e, t) {
                for (var i = 0; i < t.length; i++) {
                  var n = t[i];
                  (n.enumerable = n.enumerable || !1),
                    (n.configurable = !0),
                    'value' in n && (n.writable = !0),
                    Object.defineProperty(e, n.key, n);
                }
              }
              function u(e, t, i) {
                return (
                  t in e
                    ? Object.defineProperty(e, t, {
                        value: i,
                        enumerable: !0,
                        configurable: !0,
                        writable: !0,
                      })
                    : (e[t] = i),
                  e
                );
              }
              function c(e, t) {
                var i = Object.keys(e);
                if (Object.getOwnPropertySymbols) {
                  var n = Object.getOwnPropertySymbols(e);
                  t &&
                    (n = n.filter(function (t) {
                      return Object.getOwnPropertyDescriptor(e, t).enumerable;
                    })),
                    i.push.apply(i, n);
                }
                return i;
              }
              function f(e) {
                for (var t = 1; t < arguments.length; t++) {
                  var i = null != arguments[t] ? arguments[t] : {};
                  t % 2
                    ? c(Object(i), !0).forEach(function (t) {
                        u(e, t, i[t]);
                      })
                    : Object.getOwnPropertyDescriptors
                    ? Object.defineProperties(
                        e,
                        Object.getOwnPropertyDescriptors(i)
                      )
                    : c(Object(i)).forEach(function (t) {
                        Object.defineProperty(
                          e,
                          t,
                          Object.getOwnPropertyDescriptor(i, t)
                        );
                      });
                }
                return e;
              }
              function d(e, t) {
                (null == t || t > e.length) && (t = e.length);
                for (var i = 0, n = new Array(t); i < t; i++) n[i] = e[i];
                return n;
              }
              function p(e, t) {
                var i;
                if (
                  'undefined' == typeof Symbol ||
                  null == e[Symbol.iterator]
                ) {
                  if (
                    Array.isArray(e) ||
                    (i = (function (e, t) {
                      if (e) {
                        if ('string' == typeof e) return d(e, t);
                        var i = Object.prototype.toString.call(e).slice(8, -1);
                        return (
                          'Object' === i &&
                            e.constructor &&
                            (i = e.constructor.name),
                          'Map' === i || 'Set' === i
                            ? Array.from(e)
                            : 'Arguments' === i ||
                              /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)
                            ? d(e, t)
                            : void 0
                        );
                      }
                    })(e)) ||
                    (t && e && 'number' == typeof e.length)
                  ) {
                    i && (e = i);
                    var n = 0,
                      r = function () {};
                    return {
                      s: r,
                      n: function () {
                        return n >= e.length
                          ? {done: !0}
                          : {done: !1, value: e[n++]};
                      },
                      e: function (e) {
                        throw e;
                      },
                      f: r,
                    };
                  }
                  throw new TypeError(
                    'Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.'
                  );
                }
                var s,
                  a = !0,
                  o = !1;
                return {
                  s: function () {
                    i = e[Symbol.iterator]();
                  },
                  n: function () {
                    var e = i.next();
                    return (a = e.done), e;
                  },
                  e: function (e) {
                    (o = !0), (s = e);
                  },
                  f: function () {
                    try {
                      a || null == i.return || i.return();
                    } finally {
                      if (o) throw s;
                    }
                  },
                };
              }
              var m = 86400;
              function h(e, t) {
                return e == m && t.show2400 ? e : e % m;
              }
              var g,
                v = {
                  appendTo: 'body',
                  className: null,
                  closeOnWindowScroll: !1,
                  disableTextInput: !1,
                  disableTimeRanges: [],
                  disableTouchKeyboard: !1,
                  durationTime: null,
                  forceRoundTime: !1,
                  lang: {},
                  listWidth: null,
                  maxTime: null,
                  minTime: null,
                  noneOption: !1,
                  orientation: 'l',
                  roundingFunction: function (e, t) {
                    if (null === e) return null;
                    for (var i = 0, n = 0; n < e; ) i++, (n += 60 * t.step(i));
                    var r = n - 60 * t.step(i - 1);
                    return h(e - r < n - e ? r : n, t);
                  },
                  scrollDefault: null,
                  selectOnBlur: !1,
                  show2400: !1,
                  showDuration: !1,
                  showOn: ['click', 'focus'],
                  showOnFocus: !0,
                  step: 30,
                  stopScrollPropagation: !1,
                  timeFormat: 'g:ia',
                  typeaheadHighlight: !0,
                  useSelect: !1,
                  wrapHours: !0,
                },
                y = {
                  am: 'am',
                  pm: 'pm',
                  AM: 'AM',
                  PM: 'PM',
                  decimal: '.',
                  mins: 'mins',
                  hr: 'hr',
                  hrs: 'hrs',
                },
                b = {bubbles: !0, cancelable: !1, detail: null},
                k = (function () {
                  function e(t) {
                    var i =
                      arguments.length > 1 && void 0 !== arguments[1]
                        ? arguments[1]
                        : {};
                    o(this, e),
                      (this._handleFormatValue =
                        this._handleFormatValue.bind(this)),
                      (this._handleKeyUp = this._handleKeyUp.bind(this)),
                      (this.targetEl = t);
                    var n = e.extractAttrOptions(t, Object.keys(v));
                    this.settings = this.parseSettings(f(f(f({}, v), i), n));
                  }
                  var t, i, n;
                  return (
                    (t = e),
                    (n = [
                      {
                        key: 'extractAttrOptions',
                        value: function (e, t) {
                          var i,
                            n = {},
                            r = p(t);
                          try {
                            for (r.s(); !(i = r.n()).done; ) {
                              var s = i.value;
                              s in e.dataset && (n[s] = e.dataset[s]);
                            }
                          } catch (e) {
                            r.e(e);
                          } finally {
                            r.f();
                          }
                          return n;
                        },
                      },
                      {
                        key: 'isVisible',
                        value: function (e) {
                          var t = e[0];
                          return t.offsetWidth > 0 && t.offsetHeight > 0;
                        },
                      },
                      {
                        key: 'hideAll',
                        value: function () {
                          var e,
                            t = p(
                              document.getElementsByClassName(
                                'ui-timepicker-input'
                              )
                            );
                          try {
                            for (t.s(); !(e = t.n()).done; ) {
                              var i = e.value.timepickerObj;
                              i && i.hideMe();
                            }
                          } catch (e) {
                            t.e(e);
                          } finally {
                            t.f();
                          }
                        },
                      },
                    ]),
                    (i = [
                      {
                        key: 'hideMe',
                        value: function () {
                          if (this.settings.useSelect) this.targetEl.blur();
                          else if (this.list && e.isVisible(this.list)) {
                            this.settings.selectOnBlur && this._selectValue(),
                              this.list.hide();
                            var t = new CustomEvent('hideTimepicker', b);
                            this.targetEl.dispatchEvent(t);
                          }
                        },
                      },
                      {
                        key: '_findRow',
                        value: function (e) {
                          if (!e && 0 !== e) return !1;
                          var t = !1;
                          return (
                            (e = this.settings.roundingFunction(
                              e,
                              this.settings
                            )),
                            !!this.list &&
                              (this.list.find('li').each(function (i, n) {
                                var r = parseInt(n.dataset.time);
                                if (!isNaN(r))
                                  return r == e ? ((t = n), !1) : void 0;
                              }),
                              t)
                          );
                        },
                      },
                      {
                        key: '_hideKeyboard',
                        value: function () {
                          return (
                            (window.navigator.msMaxTouchPoints ||
                              'ontouchstart' in document) &&
                            this.settings.disableTouchKeyboard
                          );
                        },
                      },
                      {
                        key: '_setTimeValue',
                        value: function (e, t) {
                          if ('INPUT' === this.targetEl.nodeName) {
                            (null === e && '' == this.targetEl.value) ||
                              (this.targetEl.value = e);
                            var i = this;
                            i.settings.useSelect &&
                              'select' != t &&
                              i.list &&
                              i.list.val(
                                i._roundAndFormatTime(i.anytime2int(e))
                              );
                          }
                          var n = new CustomEvent('selectTime', b);
                          if (this.selectedValue != e) {
                            this.selectedValue = e;
                            var r = new CustomEvent('changeTime', b),
                              s = new CustomEvent(
                                'change',
                                Object.assign(b, {detail: 'timepicker'})
                              );
                            return (
                              'select' == t
                                ? (this.targetEl.dispatchEvent(n),
                                  this.targetEl.dispatchEvent(r),
                                  this.targetEl.dispatchEvent(s))
                                : -1 == ['error', 'initial'].indexOf(t) &&
                                  this.targetEl.dispatchEvent(r),
                              !0
                            );
                          }
                          return (
                            -1 == ['error', 'initial'].indexOf(t) &&
                              this.targetEl.dispatchEvent(n),
                            !1
                          );
                        },
                      },
                      {
                        key: '_getTimeValue',
                        value: function () {
                          return 'INPUT' === this.targetEl.nodeName
                            ? this.targetEl.value
                            : this.selectedValue;
                        },
                      },
                      {
                        key: '_selectValue',
                        value: function () {
                          var e = this;
                          e.settings;
                          var t = e.list.find('.ui-timepicker-selected');
                          if (t.hasClass('ui-timepicker-disabled')) return !1;
                          if (!t.length) return !0;
                          var i = t.get(0).dataset.time;
                          if (i) {
                            var n = parseInt(i);
                            isNaN(n) || (i = n);
                          }
                          return (
                            null !== i &&
                              ('string' != typeof i && (i = e._int2time(i)),
                              e._setTimeValue(i, 'select')),
                            !0
                          );
                        },
                      },
                      {
                        key: 'anytime2int',
                        value: function (e) {
                          return 'number' == typeof e
                            ? e
                            : 'string' == typeof e
                            ? this.time2int(e)
                            : 'object' === a(e) && e instanceof Date
                            ? 3600 * e.getHours() +
                              60 * e.getMinutes() +
                              e.getSeconds()
                            : 'function' == typeof e
                            ? e()
                            : null;
                        },
                      },
                      {
                        key: 'time2int',
                        value: function (e) {
                          if ('' === e || null == e) return null;
                          if ('now' === e) return this.anytime2int(new Date());
                          if ('string' != typeof e) return e;
                          ('a' !=
                            (e = e.toLowerCase().replace(/[\s\.]/g, '')).slice(
                              -1
                            ) &&
                            'p' != e.slice(-1)) ||
                            (e += 'm');
                          var t =
                            /^(([^0-9]*))?([0-9]?[0-9])(([0-5][0-9]))?(([0-5][0-9]))?(([^0-9]*))$/;
                          e.match(/\W/) &&
                            (t =
                              /^(([^0-9]*))?([0-9]?[0-9])(\W+([0-5][0-9]?))?(\W+([0-5][0-9]))?(([^0-9]*))$/);
                          var i = e.match(t);
                          if (!i) return null;
                          var n = parseInt(1 * i[3], 10),
                            r = i[2] || i[9],
                            s = this.parseMinuteString(i[5]),
                            a = 1 * i[7] || 0;
                          r || 2 != i[3].length || '0' != i[3][0] || (r = 'am'),
                            n > 24 &&
                              !s &&
                              ((n = 1 * i[3][0]),
                              (s = this.parseMinuteString(i[3][1])));
                          var o = n;
                          if (n <= 12 && r) {
                            var l =
                              (r = r.trim()) == this.settings.lang.pm ||
                              r == this.settings.lang.PM;
                            o = 12 == n ? (l ? 12 : 0) : n + (l ? 12 : 0);
                          } else if (
                            3600 * n + 60 * s + a >=
                            m + (this.settings.show2400 ? 1 : 0)
                          ) {
                            if (!1 === this.settings.wrapHours) return null;
                            o = n % 24;
                          }
                          var u = 3600 * o + 60 * s + a;
                          if (
                            n < 12 &&
                            !r &&
                            this.settings._twelveHourTime &&
                            this.settings.scrollDefault()
                          ) {
                            var c = u - this.settings.scrollDefault();
                            c < 0 && c >= -43200 && (u = (u + 43200) % m);
                          }
                          return u;
                        },
                      },
                      {
                        key: 'parseMinuteString',
                        value: function (e) {
                          e || (e = 0);
                          var t = 1;
                          return (
                            1 == e.length && (t = 10), parseInt(e) * t || 0
                          );
                        },
                      },
                      {
                        key: 'intStringDateOrFunc2func',
                        value: function (e) {
                          var t = this;
                          return null == e
                            ? function () {
                                return null;
                              }
                            : 'function' == typeof e
                            ? function () {
                                return t.anytime2int(e());
                              }
                            : function () {
                                return t.anytime2int(e);
                              };
                        },
                      },
                      {
                        key: 'parseSettings',
                        value: function (e) {
                          if (
                            ((e.lang = f(f({}, y), e.lang)),
                            (this.settings = e),
                            e.listWidth &&
                              (e.listWidth = this.anytime2int(e.listWidth)),
                            (e.minTime = this.intStringDateOrFunc2func(
                              e.minTime
                            )),
                            (e.maxTime = this.intStringDateOrFunc2func(
                              e.maxTime
                            )),
                            (e.durationTime = this.intStringDateOrFunc2func(
                              e.durationTime
                            )),
                            e.scrollDefault
                              ? (e.scrollDefault =
                                  this.intStringDateOrFunc2func(
                                    e.scrollDefault
                                  ))
                              : (e.scrollDefault = e.minTime),
                            'string' == typeof e.timeFormat &&
                              e.timeFormat.match(/[gh]/) &&
                              (e._twelveHourTime = !0),
                            !1 === e.showOnFocus &&
                              -1 != e.showOn.indexOf('focus') &&
                              e.showOn.splice(e.showOn.indexOf('focus'), 1),
                            'function' != typeof e.step)
                          ) {
                            var t = e.step;
                            e.step = function () {
                              return t;
                            };
                          }
                          return (
                            (e.disableTimeRanges = this._parseDisableTimeRanges(
                              e.disableTimeRanges
                            )),
                            e
                          );
                        },
                      },
                      {
                        key: '_parseDisableTimeRanges',
                        value: function (e) {
                          if (!e || 0 == e.length) return [];
                          for (var t in e)
                            e[t] = [
                              this.anytime2int(e[t][0]),
                              this.anytime2int(e[t][1]),
                            ];
                          for (
                            t =
                              (e = e.sort(function (e, t) {
                                return e[0] - t[0];
                              })).length - 1;
                            t > 0;
                            t--
                          )
                            e[t][0] <= e[t - 1][1] &&
                              ((e[t - 1] = [
                                Math.min(e[t][0], e[t - 1][0]),
                                Math.max(e[t][1], e[t - 1][1]),
                              ]),
                              e.splice(t, 1));
                          return e;
                        },
                      },
                      {
                        key: '_disableTextInputHandler',
                        value: function (e) {
                          switch (e.keyCode) {
                            case 13:
                            case 9:
                              return;
                            default:
                              e.preventDefault();
                          }
                        },
                      },
                      {
                        key: '_int2duration',
                        value: function (e, t) {
                          e = Math.abs(e);
                          var i,
                            n,
                            r = Math.round(e / 60),
                            s = [];
                          return (
                            r < 60
                              ? (s = [r, this.settings.lang.mins])
                              : ((i = Math.floor(r / 60)),
                                (n = r % 60),
                                30 == t &&
                                  30 == n &&
                                  (i += this.settings.lang.decimal + 5),
                                s.push(i),
                                s.push(
                                  1 == i
                                    ? this.settings.lang.hr
                                    : this.settings.lang.hrs
                                ),
                                30 != t &&
                                  n &&
                                  (s.push(n), s.push(this.settings.lang.mins))),
                            s.join(' ')
                          );
                        },
                      },
                      {
                        key: '_roundAndFormatTime',
                        value: function (e) {
                          if (
                            null !==
                            (e = this.settings.roundingFunction(
                              e,
                              this.settings
                            ))
                          )
                            return this._int2time(e);
                        },
                      },
                      {
                        key: '_int2time',
                        value: function (e) {
                          if ('number' != typeof e) return null;
                          var t = parseInt(e % 60),
                            i = parseInt((e / 60) % 60),
                            n = parseInt((e / 3600) % 24),
                            r = new Date(1970, 0, 2, n, i, t, 0);
                          if (isNaN(r.getTime())) return null;
                          if ('function' == typeof this.settings.timeFormat)
                            return this.settings.timeFormat(r);
                          for (
                            var s, a, o = '', l = 0;
                            l < this.settings.timeFormat.length;
                            l++
                          )
                            switch ((a = this.settings.timeFormat.charAt(l))) {
                              case 'a':
                                o +=
                                  r.getHours() > 11
                                    ? this.settings.lang.pm
                                    : this.settings.lang.am;
                                break;
                              case 'A':
                                o +=
                                  r.getHours() > 11
                                    ? this.settings.lang.PM
                                    : this.settings.lang.AM;
                                break;
                              case 'g':
                                o += 0 == (s = r.getHours() % 12) ? '12' : s;
                                break;
                              case 'G':
                                (s = r.getHours()),
                                  e === m &&
                                    (s = this.settings.show2400 ? 24 : 0),
                                  (o += s);
                                break;
                              case 'h':
                                0 != (s = r.getHours() % 12) &&
                                  s < 10 &&
                                  (s = '0' + s),
                                  (o += 0 === s ? '12' : s);
                                break;
                              case 'H':
                                (s = r.getHours()),
                                  e === m &&
                                    (s = this.settings.show2400 ? 24 : 0),
                                  (o += s > 9 ? s : '0' + s);
                                break;
                              case 'i':
                                o += (i = r.getMinutes()) > 9 ? i : '0' + i;
                                break;
                              case 's':
                                o += (t = r.getSeconds()) > 9 ? t : '0' + t;
                                break;
                              case '\\':
                                l++, (o += this.settings.timeFormat.charAt(l));
                                break;
                              default:
                                o += a;
                            }
                          return o;
                        },
                      },
                      {
                        key: '_setSelected',
                        value: function () {
                          var e = this.list;
                          e.find('li').removeClass('ui-timepicker-selected');
                          var t = this.anytime2int(this._getTimeValue());
                          if (null !== t) {
                            var i = this._findRow(t);
                            if (i) {
                              var n = i.getBoundingClientRect(),
                                r = e.get(0).getBoundingClientRect(),
                                s = n.top - r.top;
                              if (s + n.height > r.height || s < 0) {
                                var a =
                                  e.scrollTop() + (n.top - r.top) - n.height;
                                e.scrollTop(a);
                              }
                              var o = parseInt(i.dataset.time);
                              (this.settings.forceRoundTime || o === t) &&
                                i.classList.add('ui-timepicker-selected');
                            }
                          }
                        },
                      },
                      {
                        key: '_isFocused',
                        value: function (e) {
                          return e === document.activeElement;
                        },
                      },
                      {
                        key: '_handleFormatValue',
                        value: function (e) {
                          (e && 'timepicker' == e.detail) ||
                            this._formatValue(e);
                        },
                      },
                      {
                        key: '_formatValue',
                        value: function (e, t) {
                          if ('' !== this.targetEl.value) {
                            if (
                              !this._isFocused(this.targetEl) ||
                              (e && 'change' == e.type)
                            ) {
                              var i = this.settings,
                                n = this.anytime2int(this.targetEl.value);
                              if (null !== n) {
                                var r = !1;
                                null !== i.minTime &&
                                  null !== i.maxTime &&
                                  (n < i.minTime() || n > i.maxTime()) &&
                                  (r = !0);
                                var s,
                                  a = p(i.disableTimeRanges);
                                try {
                                  for (a.s(); !(s = a.n()).done; ) {
                                    var o = s.value;
                                    if (n >= o[0] && n < o[1]) {
                                      r = !0;
                                      break;
                                    }
                                  }
                                } catch (e) {
                                  a.e(e);
                                } finally {
                                  a.f();
                                }
                                if (i.forceRoundTime) {
                                  var l = i.roundingFunction(n, i);
                                  l != n && ((n = l), (t = null));
                                }
                                var u = this._int2time(n);
                                if (r) {
                                  this._setTimeValue(u);
                                  var c = new CustomEvent('timeRangeError', b);
                                  this.targetEl.dispatchEvent(c);
                                } else this._setTimeValue(u, t);
                              } else {
                                var f = new CustomEvent('timeFormatError', b);
                                this.targetEl.dispatchEvent(f);
                              }
                            }
                          } else this._setTimeValue(null, t);
                        },
                      },
                      {
                        key: '_generateNoneElement',
                        value: function (e, t) {
                          var i, n, r, s;
                          return (
                            'object' == a(e)
                              ? ((i = e.label),
                                (n = e.className),
                                (r = e.value))
                              : 'string' == typeof e
                              ? ((i = e), (r = ''))
                              : $.error('Invalid noneOption value'),
                            t
                              ? ((s = document.createElement('option')).value =
                                  r)
                              : ((s =
                                  document.createElement('li')).dataset.time =
                                  String(r)),
                            (s.innerText = i),
                            s.classList.add(n),
                            s
                          );
                        },
                      },
                      {
                        key: '_handleKeyUp',
                        value: function (t) {
                          var i = this;
                          if (
                            !this.list ||
                            !e.isVisible(this.list) ||
                            this.settings.disableTextInput
                          )
                            return !0;
                          if ('paste' !== t.type && 'cut' !== t.type)
                            switch (t.keyCode) {
                              case 96:
                              case 97:
                              case 98:
                              case 99:
                              case 100:
                              case 101:
                              case 102:
                              case 103:
                              case 104:
                              case 105:
                              case 48:
                              case 49:
                              case 50:
                              case 51:
                              case 52:
                              case 53:
                              case 54:
                              case 55:
                              case 56:
                              case 57:
                              case 65:
                              case 77:
                              case 80:
                              case 186:
                              case 8:
                              case 46:
                                this.settings.typeaheadHighlight
                                  ? this._setSelected()
                                  : this.list.hide();
                            }
                          else
                            setTimeout(function () {
                              i.settings.typeaheadHighlight
                                ? i._setSelected()
                                : i.list.hide();
                            }, 0);
                        },
                      },
                    ]) && l(t.prototype, i),
                    n && l(t, n),
                    e
                  );
                })();
              function T(e) {
                return Array.isArray(e)
                  ? e.map(T)
                  : !0 === e
                  ? {label: 'None', value: ''}
                  : 'object' === a(e)
                  ? e
                  : {label: e, value: ''};
              }
              function w(e) {
                var t = document.createElement('option');
                return (
                  (t.value = e.label),
                  e.duration
                    ? t.appendChild(
                        document.createTextNode(
                          e.label + ' (' + e.duration + ')'
                        )
                      )
                    : t.appendChild(document.createTextNode(e.label)),
                  e.disabled && (t.disabled = !0),
                  t
                );
              }
              function O(e) {
                var t = document.createElement('li');
                if (
                  ((t.dataset.time = e.value),
                  e.className && t.classList.add(e.className),
                  (t.className = e.className),
                  t.appendChild(document.createTextNode(e.label)),
                  e.duration)
                ) {
                  var i = document.createElement('span');
                  i.appendChild(
                    document.createTextNode('(' + e.duration + ')')
                  ),
                    i.classList.add('ui-timepicker-duration'),
                    t.appendChild(i);
                }
                return (
                  e.disabled && t.classList.add('ui-timepicker-disabled'), t
                );
              }
              !(function () {
                if ('function' == typeof window.CustomEvent) return !1;
                window.CustomEvent = function (e, t) {
                  t || (t = {}), (t = Object.assign(b, t));
                  var i = document.createEvent('CustomEvent');
                  return (
                    i.initCustomEvent(e, t.bubbles, t.cancelable, t.detail), i
                  );
                };
              })(),
                (g = function (e) {
                  var t = {
                    init: function (n) {
                      return this.each(function () {
                        var s = e(this),
                          a = new k(this, n),
                          o = a.settings;
                        if (
                          (o.lang,
                          (this.timepickerObj = a),
                          s.addClass('ui-timepicker-input'),
                          o.useSelect)
                        )
                          i(s);
                        else {
                          if ((s.prop('autocomplete', 'off'), o.showOn))
                            for (var l in o.showOn)
                              s.on(o.showOn[l] + '.timepicker', t.show);
                          s.on('change.timepicker', a._handleFormatValue),
                            s.on('keydown.timepicker', r),
                            s.on('keyup.timepicker', a._handleKeyUp),
                            o.disableTextInput &&
                              s.on(
                                'keydown.timepicker',
                                a._disableTextInputHandler
                              ),
                            s.on('cut.timepicker', a._handleKeyUp),
                            s.on('paste.timepicker', a._handleKeyUp),
                            a._formatValue(null, 'initial');
                        }
                      });
                    },
                    show: function (t) {
                      var r = e(this),
                        s = r[0].timepickerObj,
                        a = s.settings;
                      if ((t && t.preventDefault(), a.useSelect))
                        s.list.trigger('focus');
                      else {
                        s._hideKeyboard() && r.trigger('blur');
                        var o = s.list;
                        if (
                          !r.prop('readonly') &&
                          (i(r), (o = s.list), !k.isVisible(o))
                        ) {
                          r.is('input') && (s.selectedValue = r.val()),
                            s._setSelected(),
                            k.hideAll(),
                            'number' == typeof a.listWidth &&
                              o.width(r.outerWidth() * a.listWidth),
                            o.show();
                          var l = {};
                          a.orientation.match(/r/)
                            ? (l.left =
                                r.offset().left +
                                r.outerWidth() -
                                o.outerWidth() +
                                parseInt(
                                  o.css('marginLeft').replace('px', ''),
                                  10
                                ))
                            : a.orientation.match(/l/)
                            ? (l.left =
                                r.offset().left +
                                parseInt(
                                  o.css('marginLeft').replace('px', ''),
                                  10
                                ))
                            : a.orientation.match(/c/) &&
                              (l.left =
                                r.offset().left +
                                (r.outerWidth() - o.outerWidth()) / 2 +
                                parseInt(
                                  o.css('marginLeft').replace('px', ''),
                                  10
                                )),
                            't' ==
                            (a.orientation.match(/t/)
                              ? 't'
                              : a.orientation.match(/b/)
                              ? 'b'
                              : r.offset().top +
                                  r.outerHeight(!0) +
                                  o.outerHeight() >
                                e(window).height() + e(window).scrollTop()
                              ? 't'
                              : 'b')
                              ? (o.addClass('ui-timepicker-positioned-top'),
                                (l.top =
                                  r.offset().top -
                                  o.outerHeight() +
                                  parseInt(
                                    o.css('marginTop').replace('px', ''),
                                    10
                                  )))
                              : (o.removeClass('ui-timepicker-positioned-top'),
                                (l.top =
                                  r.offset().top +
                                  r.outerHeight() +
                                  parseInt(
                                    o.css('marginTop').replace('px', ''),
                                    10
                                  ))),
                            o.offset(l);
                          var u = o.find('.ui-timepicker-selected');
                          if (!u.length) {
                            var c = s.anytime2int(s._getTimeValue());
                            null !== c
                              ? (u = e(s._findRow(c)))
                              : a.scrollDefault() &&
                                (u = e(s._findRow(a.scrollDefault())));
                          }
                          if (
                            ((u.length &&
                              !u.hasClass('ui-timepicker-disabled')) ||
                              (u = o.find(
                                'li:not(.ui-timepicker-disabled):first'
                              )),
                            u && u.length)
                          ) {
                            var f =
                              o.scrollTop() +
                              u.position().top -
                              u.outerHeight();
                            o.scrollTop(f);
                          } else o.scrollTop(0);
                          return (
                            a.stopScrollPropagation &&
                              e(document).on(
                                'wheel.ui-timepicker',
                                '.ui-timepicker-wrapper',
                                function (t) {
                                  t.preventDefault();
                                  var i = e(this).scrollTop();
                                  e(this).scrollTop(i + t.originalEvent.deltaY);
                                }
                              ),
                            e(document).on('mousedown.ui-timepicker', n),
                            window.addEventListener('resize', n),
                            a.closeOnWindowScroll &&
                              e(document).on('scroll.ui-timepicker', n),
                            r.trigger('showTimepicker'),
                            this
                          );
                        }
                      }
                    },
                    hide: function (e) {
                      var t = this[0].timepickerObj;
                      return t && t.hideMe(), k.hideAll(), this;
                    },
                    option: function (t, n) {
                      return 'string' == typeof t && void 0 === n
                        ? this[0].timepickerObj.settings[t]
                        : this.each(function () {
                            var r = e(this),
                              s = r[0].timepickerObj,
                              o = s.settings,
                              l = s.list;
                            'object' == a(t)
                              ? (o = e.extend(o, t))
                              : 'string' == typeof t && (o[t] = n),
                              (o = s.parseSettings(o)),
                              (s.settings = o),
                              s._formatValue({type: 'change'}, 'initial'),
                              l && (l.remove(), (s.list = null)),
                              o.useSelect && i(r);
                          });
                    },
                    getSecondsFromMidnight: function () {
                      var e = this[0].timepickerObj;
                      return e.anytime2int(e._getTimeValue());
                    },
                    getTime: function (e) {
                      var t = this[0].timepickerObj,
                        i = t._getTimeValue();
                      if (!i) return null;
                      var n = t.anytime2int(i);
                      if (null === n) return null;
                      e || (e = new Date());
                      var r = new Date(e);
                      return (
                        r.setHours(n / 3600),
                        r.setMinutes((n % 3600) / 60),
                        r.setSeconds(n % 60),
                        r.setMilliseconds(0),
                        r
                      );
                    },
                    isVisible: function () {
                      var e = this[0].timepickerObj;
                      return !!(e && e.list && k.isVisible(e.list));
                    },
                    setTime: function (e) {
                      var t = this[0].timepickerObj,
                        i = t.settings;
                      if (i.forceRoundTime)
                        var n = t._roundAndFormatTime(t.anytime2int(e));
                      else n = t._int2time(t.anytime2int(e));
                      return (
                        e && null === n && i.noneOption && (n = e),
                        t._setTimeValue(n, 'initial'),
                        t._formatValue({type: 'change'}, 'initial'),
                        t && t.list && t._setSelected(),
                        this
                      );
                    },
                    remove: function () {
                      var e = this;
                      if (e.hasClass('ui-timepicker-input')) {
                        var t = e[0].timepickerObj,
                          i = t.settings;
                        return (
                          e.removeAttr('autocomplete', 'off'),
                          e.removeClass('ui-timepicker-input'),
                          e.removeData('timepicker-obj'),
                          e.off('.timepicker'),
                          t.list && t.list.remove(),
                          i.useSelect && e.show(),
                          (t.list = null),
                          this
                        );
                      }
                    },
                  };
                  function i(i) {
                    var n = i[0].timepickerObj,
                      r = n.list,
                      s = n.settings;
                    r && r.length && (r.remove(), (n.list = null));
                    var a = e(
                      (function (e) {
                        var t,
                          i = [].concat(
                            (function (e) {
                              if (!e.noneOption) return [];
                              var t = T(e.noneOption);
                              return Array.isArray(e.noneOption) ? t : [t];
                            })(e.settings),
                            (function (e) {
                              var t,
                                i,
                                n = e.settings,
                                r =
                                  null !== (t = n.minTime()) && void 0 !== t
                                    ? t
                                    : 0,
                                s =
                                  null !== (i = n.maxTime()) && void 0 !== i
                                    ? i
                                    : r + m - 1;
                              s < r && (s += m),
                                86399 === s &&
                                  'string' == typeof n.timeFormat &&
                                  n.show2400 &&
                                  (s = m);
                              for (
                                var a = [], o = r, l = 0;
                                o <= s;
                                l++, o += 60 * n.step(l)
                              ) {
                                var u = o,
                                  c = e._int2time(u),
                                  f =
                                    u % m < 43200
                                      ? 'ui-timepicker-am'
                                      : 'ui-timepicker-pm',
                                  d = {label: c, value: h(u, n), className: f};
                                if (
                                  (null !== n.minTime() ||
                                    null !== n.durationTime()) &&
                                  n.showDuration
                                ) {
                                  var g,
                                    v =
                                      null !== (g = n.durationTime()) &&
                                      void 0 !== g
                                        ? g
                                        : n.minTime(),
                                    y = e._int2duration(o - v, n.step());
                                  d.duration = y;
                                }
                                var b,
                                  k = p(n.disableTimeRanges);
                                try {
                                  for (k.s(); !(b = k.n()).done; ) {
                                    var T = b.value;
                                    if (u % m >= T[0] && u % m < T[1]) {
                                      d.disabled = !0;
                                      break;
                                    }
                                  }
                                } catch (e) {
                                  k.e(e);
                                } finally {
                                  k.f();
                                }
                                a.push(d);
                              }
                              return a;
                            })(e)
                          );
                        if (
                          ((t = e.settings.useSelect
                            ? (function (e, t) {
                                var i = document.createElement('select');
                                i.classList.add('ui-timepicker-select'),
                                  t && (i.name = 'ui-timepicker-' + t);
                                var n,
                                  r = p(e);
                                try {
                                  for (r.s(); !(n = r.n()).done; ) {
                                    var s = w(n.value);
                                    i.appendChild(s);
                                  }
                                } catch (e) {
                                  r.e(e);
                                } finally {
                                  r.f();
                                }
                                return i;
                              })(i, e.targetEl.name)
                            : (function (e) {
                                var t = document.createElement('ul');
                                t.classList.add('ui-timepicker-list');
                                var i,
                                  n = p(e);
                                try {
                                  for (n.s(); !(i = n.n()).done; ) {
                                    var r = O(i.value);
                                    t.appendChild(r);
                                  }
                                } catch (e) {
                                  n.e(e);
                                } finally {
                                  n.f();
                                }
                                var s = document.createElement('div');
                                return (
                                  s.classList.add('ui-timepicker-wrapper'),
                                  (s.tabIndex = -1),
                                  (s.style.display = 'none'),
                                  (s.style.position = 'absolute'),
                                  s.appendChild(t),
                                  s
                                );
                              })(i)),
                          e.settings.className)
                        ) {
                          var n,
                            r = p(e.settings.className.split(' '));
                          try {
                            for (r.s(); !(n = r.n()).done; ) {
                              var s = n.value;
                              t.classList.add(s);
                            }
                          } catch (e) {
                            r.e(e);
                          } finally {
                            r.f();
                          }
                        }
                        return (
                          !e.settings.showDuration ||
                            (null === e.settings.minTime &&
                              null === e.settings.durationTime) ||
                            (t.classList.add('ui-timepicker-with-duration'),
                            t.classList.add(
                              'ui-timepicker-step-' + e.settings.step()
                            )),
                          t
                        );
                      })(n)
                    );
                    if (
                      ((r = s.useSelect ? a : a.children('ul')),
                      a.data('timepicker-input', i),
                      (n.list = a),
                      s.useSelect)
                    )
                      i.val() &&
                        r.val(n._roundAndFormatTime(n.anytime2int(i.val()))),
                        r.on('focus', function () {
                          e(this)
                            .data('timepicker-input')
                            .trigger('showTimepicker');
                        }),
                        r.on('blur', function () {
                          e(this)
                            .data('timepicker-input')
                            .trigger('hideTimepicker');
                        }),
                        r.on('change', function () {
                          n._setTimeValue(e(this).val(), 'select');
                        }),
                        n._setTimeValue(r.val(), 'initial'),
                        i.hide().after(r);
                    else {
                      var o = s.appendTo;
                      'string' == typeof o
                        ? (o = e(o))
                        : 'function' == typeof o && (o = o(i)),
                        o.append(a),
                        n._setSelected(),
                        r.on('mousedown click', 'li', function (s) {
                          i.off('focus.timepicker'),
                            i.on('focus.timepicker-ie-hack', function () {
                              i.off('focus.timepicker-ie-hack'),
                                i.on('focus.timepicker', t.show);
                            }),
                            n._hideKeyboard() || i[0].focus(),
                            r.find('li').removeClass('ui-timepicker-selected'),
                            e(this).addClass('ui-timepicker-selected'),
                            n._selectValue() &&
                              (i.trigger('hideTimepicker'),
                              r.on(
                                'mouseup.timepicker click.timepicker',
                                'li',
                                function (e) {
                                  r.off('mouseup.timepicker click.timepicker'),
                                    a.hide();
                                }
                              ));
                        });
                    }
                  }
                  function n(t) {
                    if ('focus' != t.type || t.target != window) {
                      var i = e(t.target);
                      i.closest('.ui-timepicker-input').length ||
                        i.closest('.ui-timepicker-wrapper').length ||
                        (k.hideAll(),
                        e(document).off('.ui-timepicker'),
                        e(window).off('.ui-timepicker'));
                    }
                  }
                  function r(i) {
                    var n = e(this),
                      r = n[0].timepickerObj,
                      s = r.list;
                    if (!s || !k.isVisible(s)) {
                      if (40 != i.keyCode) return !0;
                      t.show.call(n.get(0)),
                        (s = r.list),
                        r._hideKeyboard() || n.trigger('focus');
                    }
                    switch (i.keyCode) {
                      case 13:
                        return (
                          r._selectValue() &&
                            (r._formatValue({type: 'change'}), r.hideMe()),
                          i.preventDefault(),
                          !1
                        );
                      case 38:
                        var a = s.find('.ui-timepicker-selected');
                        return (
                          a.length
                            ? a.is(':first-child') ||
                              (a.removeClass('ui-timepicker-selected'),
                              a.prev().addClass('ui-timepicker-selected'),
                              a.prev().position().top < a.outerHeight() &&
                                s.scrollTop(s.scrollTop() - a.outerHeight()))
                            : (s.find('li').each(function (t, i) {
                                if (e(i).position().top > 0)
                                  return (a = e(i)), !1;
                              }),
                              a.addClass('ui-timepicker-selected')),
                          !1
                        );
                      case 40:
                        return (
                          0 === (a = s.find('.ui-timepicker-selected')).length
                            ? (s.find('li').each(function (t, i) {
                                if (e(i).position().top > 0)
                                  return (a = e(i)), !1;
                              }),
                              a.addClass('ui-timepicker-selected'))
                            : a.is(':last-child') ||
                              (a.removeClass('ui-timepicker-selected'),
                              a.next().addClass('ui-timepicker-selected'),
                              a.next().position().top + 2 * a.outerHeight() >
                                s.outerHeight() &&
                                s.scrollTop(s.scrollTop() + a.outerHeight())),
                          !1
                        );
                      case 27:
                        s.find('li').removeClass('ui-timepicker-selected'),
                          r.hideMe();
                        break;
                      case 9:
                        r.hideMe();
                        break;
                      default:
                        return !0;
                    }
                  }
                  (e.fn.timepicker = function (i) {
                    return this.length
                      ? t[i]
                        ? this.hasClass('ui-timepicker-input')
                          ? t[i].apply(
                              this,
                              Array.prototype.slice.call(arguments, 1)
                            )
                          : this
                        : 'object' !== a(i) && i
                        ? void e.error(
                            'Method ' +
                              i +
                              ' does not exist on jQuery.timepicker'
                          )
                        : t.init.apply(this, arguments)
                      : this;
                  }),
                    (e.fn.timepicker.defaults = v);
                }),
                'object' === a(t) &&
                t &&
                'object' === a(e) &&
                e &&
                e.exports === t
                  ? g(i(1145))
                  : ((r = [i(1145)]),
                    void 0 ===
                      (s = 'function' == typeof (n = g) ? n.apply(t, r) : n) ||
                      (e.exports = s));
            })();
        },
        1145: function (t) {
          'use strict';
          t.exports = e;
        },
      },
      i = {};
    function n(e) {
      var r = i[e];
      if (void 0 !== r) return r.exports;
      var s = (i[e] = {id: e, loaded: !1, exports: {}});
      return t[e](s, s.exports, n), (s.loaded = !0), s.exports;
    }
    (n.n = function (e) {
      var t =
        e && e.__esModule
          ? function () {
              return e.default;
            }
          : function () {
              return e;
            };
      return n.d(t, {a: t}), t;
    }),
      (n.d = function (e, t) {
        for (var i in t)
          n.o(t, i) &&
            !n.o(e, i) &&
            Object.defineProperty(e, i, {enumerable: !0, get: t[i]});
      }),
      (n.o = function (e, t) {
        return Object.prototype.hasOwnProperty.call(e, t);
      }),
      (n.r = function (e) {
        'undefined' != typeof Symbol &&
          Symbol.toStringTag &&
          Object.defineProperty(e, Symbol.toStringTag, {value: 'Module'}),
          Object.defineProperty(e, '__esModule', {value: !0});
      }),
      (n.nmd = function (e) {
        return (e.paths = []), e.children || (e.children = []), e;
      });
    var r = {};
    return (
      (function () {
        'use strict';
        n.r(r), n(7775);
      })(),
      r
    );
  })();
});
