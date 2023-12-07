import requests
import random
import json
import re
import copy
import pythonmonkey as pm
from pprint import pprint
import inquirer

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse

# Fixed DdddOcr ANTIALIAS problem.
# Message: AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'
# * Related:
#    - TransparentLC: https://github.com/sml2h3/ddddocr/issues/142

from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    setattr(Image, 'ANTIALIAS', Image.LANCZOS)
import ddddocr

# Fixed Javascript Code.
FIXED_JAVASCRIPT = """
const NewWindow = {};

function getRandomValues (array) {
 for (let i = 0, r; i < array.length; i++) {
    if ((i & 0x03) === 0) r = Math.random() * 0x100000000
    array[i] = (r >>> ((i & 0x03) << 3)) & 0xff
  }

  return array
}

function e(t, e, i) {
  null != t &&
    ('number' == typeof t
      ? this.fromNumber(t, e, i)
      : null == e && 'string' != typeof t
      ? this.fromString(t, 256)
      : this.fromString(t, e))
}
function i() {
  return new e(null)
}
function r(t, e, i, r, s, n) {
  for (; --n >= 0; ) {
    var o = e * this[t++] + i[r] + s
    s = Math.floor(o / 67108864)
    i[r++] = 67108863 & o
  }
  return s
}
function s(t, e, i, r, s, n) {
  for (var o = 32767 & e, h = e >> 15; --n >= 0; ) {
    var a = 32767 & this[t],
      u = this[t++] >> 15,
      c = h * a + u * o
    a = o * a + ((32767 & c) << 15) + i[r] + (1073741823 & s)
    s = (a >>> 30) + (c >>> 15) + h * u + (s >>> 30)
    i[r++] = 1073741823 & a
  }
  return s
}
function n(t, e, i, r, s, n) {
  for (var o = 16383 & e, h = e >> 14; --n >= 0; ) {
    var a = 16383 & this[t],
      u = this[t++] >> 14,
      c = h * a + u * o
    a = o * a + ((16383 & c) << 14) + i[r] + s
    s = (a >> 28) + (c >> 14) + h * u
    i[r++] = 268435455 & a
  }
  return s
}
function o(t) {
  return Be.charAt(t)
}
function h(t, e) {
  var i = Ke[t.charCodeAt(e)]
  return null == i ? -1 : i
}
function a(t) {
  for (var e = this.t - 1; e >= 0; --e) {
    t[e] = this[e]
  }
  t.t = this.t
  t.s = this.s
}
function u(t) {
  this.t = 1
  this.s = 0 > t ? -1 : 0
  t > 0 ? (this[0] = t) : -1 > t ? (this[0] = t + this.DV) : (this.t = 0)
}
function c(t) {
  var e = i()
  return e.fromInt(t), e
}
function f(t, i) {
  var r
  if (16 == i) {
    r = 4
  } else {
    if (8 == i) {
      r = 3
    } else {
      if (256 == i) {
        r = 8
      } else {
        if (2 == i) {
          r = 1
        } else {
          if (32 == i) {
            r = 5
          } else {
            if (4 != i) {
              return void this.fromRadix(t, i)
            }
            r = 2
          }
        }
      }
    }
  }
  this.t = 0
  this.s = 0
  for (var s = t.length, n = false, o = 0; --s >= 0; ) {
    var a = 8 == r ? 255 & t[s] : h(t, s)
    0 > a
      ? '-' == t.charAt(s) && (n = true)
      : ((n = false),
        0 == o
          ? (this[this.t++] = a)
          : o + r > this.DB
          ? ((this[this.t - 1] |= (a & ((1 << (this.DB - o)) - 1)) << o),
            (this[this.t++] = a >> (this.DB - o)))
          : (this[this.t - 1] |= a << o),
        (o += r),
        o >= this.DB && (o -= this.DB))
  }
  8 == r &&
    0 != (128 & t[0]) &&
    ((this.s = -1),
    o > 0 && (this[this.t - 1] |= ((1 << (this.DB - o)) - 1) << o))
  this.clamp()
  n && e.ZERO.subTo(this, this)
}
function p() {
  for (var t = this.s & this.DM; this.t > 0 && this[this.t - 1] == t; ) {
    --this.t
  }
}
function l(t) {
  if (this.s < 0) {
    return '-' + this.negate().toString(t)
  }
  var e
  if (16 == t) {
    e = 4
  } else {
    if (8 == t) {
      e = 3
    } else {
      if (2 == t) {
        e = 1
      } else {
        if (32 == t) {
          e = 5
        } else {
          if (4 != t) {
            return this.toRadix(t)
          }
          e = 2
        }
      }
    }
  }
  var i,
    r = (1 << e) - 1,
    s = false,
    n = '',
    h = this.t,
    a = this.DB - ((h * this.DB) % e)
  if (h-- > 0) {
    for (
      a < this.DB && (i = this[h] >> a) > 0 && ((s = true), (n = o(i)));
      h >= 0;

    ) {
      e > a
        ? ((i = (this[h] & ((1 << a) - 1)) << (e - a)),
          (i |= this[--h] >> (a += this.DB - e)))
        : ((i = (this[h] >> (a -= e)) & r), 0 >= a && ((a += this.DB), --h))
      i > 0 && (s = true)
      s && (n += o(i))
    }
  }
  return s ? n : '0'
}
function d() {
  var t = i()
  return e.ZERO.subTo(this, t), t
}
function g() {
  return this.s < 0 ? this.negate() : this
}
function m(t) {
  var e = this.s - t.s
  if (0 != e) {
    return e
  }
  var i = this.t
  if (((e = i - t.t), 0 != e)) {
    return this.s < 0 ? -e : e
  }
  for (; --i >= 0; ) {
    if (0 != (e = this[i] - t[i])) {
      return e
    }
  }
  return 0
}
function y(t) {
  var e,
    i = 1
  return (
    0 != (e = t >>> 16) && ((t = e), (i += 16)),
    0 != (e = t >> 8) && ((t = e), (i += 8)),
    0 != (e = t >> 4) && ((t = e), (i += 4)),
    0 != (e = t >> 2) && ((t = e), (i += 2)),
    0 != (e = t >> 1) && ((t = e), (i += 1)),
    i
  )
}
function b() {
  return this.t <= 0
    ? 0
    : this.DB * (this.t - 1) + y(this[this.t - 1] ^ (this.s & this.DM))
}
function T(t, e) {
  var i
  for (i = this.t - 1; i >= 0; --i) {
    e[i + t] = this[i]
  }
  for (i = t - 1; i >= 0; --i) {
    e[i] = 0
  }
  e.t = this.t + t
  e.s = this.s
}
function S(t, e) {
  for (var i = t; i < this.t; ++i) {
    e[i - t] = this[i]
  }
  e.t = Math.max(this.t - t, 0)
  e.s = this.s
}
function R(t, e) {
  var i,
    r = t % this.DB,
    s = this.DB - r,
    n = (1 << s) - 1,
    o = Math.floor(t / this.DB),
    h = (this.s << r) & this.DM
  for (i = this.t - 1; i >= 0; --i) {
    e[i + o + 1] = (this[i] >> s) | h
    h = (this[i] & n) << r
  }
  for (i = o - 1; i >= 0; --i) {
    e[i] = 0
  }
  e[o] = h
  e.t = this.t + o + 1
  e.s = this.s
  e.clamp()
}
function E(t, e) {
  e.s = this.s
  var i = Math.floor(t / this.DB)
  if (i >= this.t) {
    return void (e.t = 0)
  }
  var r = t % this.DB,
    s = this.DB - r,
    n = (1 << r) - 1
  e[0] = this[i] >> r
  for (var o = i + 1; o < this.t; ++o) {
    e[o - i - 1] |= (this[o] & n) << s
    e[o - i] = this[o] >> r
  }
  r > 0 && (e[this.t - i - 1] |= (this.s & n) << s)
  e.t = this.t - i
  e.clamp()
}
function D(t, e) {
  for (var i = 0, r = 0, s = Math.min(t.t, this.t); s > i; ) {
    r += this[i] - t[i]
    e[i++] = r & this.DM
    r >>= this.DB
  }
  if (t.t < this.t) {
    for (r -= t.s; i < this.t; ) {
      r += this[i]
      e[i++] = r & this.DM
      r >>= this.DB
    }
    r += this.s
  } else {
    for (r += this.s; i < t.t; ) {
      r -= t[i]
      e[i++] = r & this.DM
      r >>= this.DB
    }
    r -= t.s
  }
  e.s = 0 > r ? -1 : 0
  ;-1 > r ? (e[i++] = this.DV + r) : r > 0 && (e[i++] = r)
  e.t = i
  e.clamp()
}
function w(t, i) {
  var r = this.abs(),
    s = t.abs(),
    n = r.t
  for (i.t = n + s.t; --n >= 0; ) {
    i[n] = 0
  }
  for (n = 0; n < s.t; ++n) {
    i[n + r.t] = r.am(0, s[n], i, n, 0, r.t)
  }
  i.s = 0
  i.clamp()
  this.s != t.s && e.ZERO.subTo(i, i)
}
function x(t) {
  for (var e = this.abs(), i = (t.t = 2 * e.t); --i >= 0; ) {
    t[i] = 0
  }
  for (i = 0; i < e.t - 1; ++i) {
    var r = e.am(i, e[i], t, 2 * i, 0, 1)
    ;(t[i + e.t] += e.am(i + 1, 2 * e[i], t, 2 * i + 1, r, e.t - i - 1)) >=
      e.DV && ((t[i + e.t] -= e.DV), (t[i + e.t + 1] = 1))
  }
  t.t > 0 && (t[t.t - 1] += e.am(i, e[i], t, 2 * i, 0, 1))
  t.s = 0
  t.clamp()
}
function B(t, r, s) {
  var n = t.abs()
  if (!(n.t <= 0)) {
    var o = this.abs()
    if (o.t < n.t) {
      return null != r && r.fromInt(0), void (null != s && this.copyTo(s))
    }
    null == s && (s = i())
    var h = i(),
      a = this.s,
      u = t.s,
      c = this.DB - y(n[n.t - 1])
    c > 0 ? (n.lShiftTo(c, h), o.lShiftTo(c, s)) : (n.copyTo(h), o.copyTo(s))
    var f = h.t,
      p = h[f - 1]
    if (0 != p) {
      var l = p * (1 << this.F1) + (f > 1 ? h[f - 2] >> this.F2 : 0),
        d = this.FV / l,
        g = (1 << this.F1) / l,
        m = 1 << this.F2,
        v = s.t,
        b = v - f,
        T = null == r ? i() : r
      for (
        h.dlShiftTo(b, T),
          s.compareTo(T) >= 0 && ((s[s.t++] = 1), s.subTo(T, s)),
          e.ONE.dlShiftTo(f, T),
          T.subTo(h, h);
        h.t < f;

      ) {
        h[h.t++] = 0
      }
      for (; --b >= 0; ) {
        var S =
          s[--v] == p ? this.DM : Math.floor(s[v] * d + (s[v - 1] + m) * g)
        if ((s[v] += h.am(0, S, s, b, 0, f)) < S) {
          for (h.dlShiftTo(b, T), s.subTo(T, s); s[v] < --S; ) {
            s.subTo(T, s)
          }
        }
      }
      null != r && (s.drShiftTo(f, r), a != u && e.ZERO.subTo(r, r))
      s.t = f
      s.clamp()
      c > 0 && s.rShiftTo(c, s)
      0 > a && e.ZERO.subTo(s, s)
    }
  }
}
function K(t) {
  var r = i()
  return (
    this.abs().divRemTo(t, null, r),
    this.s < 0 && r.compareTo(e.ZERO) > 0 && t.subTo(r, r),
    r
  )
}
function A(t) {
  this.m = t
}
function U(t) {
  return t.s < 0 || t.compareTo(this.m) >= 0 ? t.mod(this.m) : t
}
function O(t) {
  return t
}
function V(t) {
  t.divRemTo(this.m, null, t)
}
function N(t, e, i) {
  t.multiplyTo(e, i)
  this.reduce(i)
}
function J(t, e) {
  t.squareTo(e)
  this.reduce(e)
}
function I() {
  if (this.t < 1) {
    return 0
  }
  var t = this[0]
  if (0 == (1 & t)) {
    return 0
  }
  var e = 3 & t
  return (
    (e = (e * (2 - (15 & t) * e)) & 15),
    (e = (e * (2 - (255 & t) * e)) & 255),
    (e = (e * (2 - (((65535 & t) * e) & 65535))) & 65535),
    (e = (e * (2 - ((t * e) % this.DV))) % this.DV),
    e > 0 ? this.DV - e : -e
  )
}
function P(t) {
  this.m = t
  this.mp = t.invDigit()
  this.mpl = 32767 & this.mp
  this.mph = this.mp >> 15
  this.um = (1 << (t.DB - 15)) - 1
  this.mt2 = 2 * t.t
}
function M(t) {
  var r = i()
  return (
    t.abs().dlShiftTo(this.m.t, r),
    r.divRemTo(this.m, null, r),
    t.s < 0 && r.compareTo(e.ZERO) > 0 && this.m.subTo(r, r),
    r
  )
}
function L(t) {
  var e = i()
  return t.copyTo(e), this.reduce(e), e
}
function q(t) {
  for (; t.t <= this.mt2; ) {
    t[t.t++] = 0
  }
  for (var e = 0; e < this.m.t; ++e) {
    var i = 32767 & t[e],
      r =
        (i * this.mpl +
          (((i * this.mph + (t[e] >> 15) * this.mpl) & this.um) << 15)) &
        t.DM
    for (
      i = e + this.m.t, t[i] += this.m.am(0, r, t, e, 0, this.m.t);
      t[i] >= t.DV;

    ) {
      t[i] -= t.DV
      t[++i]++
    }
  }
  t.clamp()
  t.drShiftTo(this.m.t, t)
  t.compareTo(this.m) >= 0 && t.subTo(this.m, t)
}
function C(t, e) {
  t.squareTo(e)
  this.reduce(e)
}
function H(t, e, i) {
  t.multiplyTo(e, i)
  this.reduce(i)
}
function j() {
  return 0 == (this.t > 0 ? 1 & this[0] : this.s)
}
function k(t, r) {
  if (t > 4294967295 || 1 > t) {
    return e.ONE
  }
  var s = i(),
    n = i(),
    o = r.convert(this),
    h = y(t) - 1
  for (o.copyTo(s); --h >= 0; ) {
    if ((r.sqrTo(s, n), (t & (1 << h)) > 0)) {
      r.mulTo(n, o, s)
    } else {
      var a = s
      s = n
      n = a
    }
  }
  return r.revert(s)
}
function F(t, e) {
  var i
  return (i = 256 > t || e.isEven() ? new A(e) : new P(e)), this.exp(t, i)
}
function _() {
  var t = i()
  return this.copyTo(t), t
}
function z() {
  if (this.s < 0) {
    if (1 == this.t) {
      return this[0] - this.DV
    }
    if (0 == this.t) {
      return -1
    }
  } else {
    if (1 == this.t) {
      return this[0]
    }
    if (0 == this.t) {
      return 0
    }
  }
  return ((this[1] & ((1 << (32 - this.DB)) - 1)) << this.DB) | this[0]
}
function Z() {
  return 0 == this.t ? this.s : (this[0] << 24) >> 24
}
function G() {
  return 0 == this.t ? this.s : (this[0] << 16) >> 16
}
function $(t) {
  return Math.floor((Math.LN2 * this.DB) / Math.log(t))
}
function Y() {
  return this.s < 0 ? -1 : this.t <= 0 || (1 == this.t && this[0] <= 0) ? 0 : 1
}
function W(t) {
  if ((null == t && (t = 10), 0 == this.signum() || 2 > t || t > 36)) {
    return '0'
  }
  var e = this.chunkSize(t),
    r = Math.pow(t, e),
    s = c(r),
    n = i(),
    o = i(),
    h = ''
  for (this.divRemTo(s, n, o); n.signum() > 0; ) {
    h = (r + o.intValue()).toString(t).substr(1) + h
    n.divRemTo(s, n, o)
  }
  return o.intValue().toString(t) + h
}
function Q(t, i) {
  this.fromInt(0)
  null == i && (i = 10)
  for (
    var r = this.chunkSize(i),
      s = Math.pow(i, r),
      n = false,
      o = 0,
      a = 0,
      u = 0;
    u < t.length;
    ++u
  ) {
    var c = h(t, u)
    0 > c
      ? '-' == t.charAt(u) && 0 == this.signum() && (n = true)
      : ((a = i * a + c),
        ++o >= r &&
          (this.dMultiply(s), this.dAddOffset(a, 0), (o = 0), (a = 0)))
  }
  o > 0 && (this.dMultiply(Math.pow(i, o)), this.dAddOffset(a, 0))
  n && e.ZERO.subTo(this, this)
}
function X(t, i, r) {
  if ('number' == typeof i) {
    if (2 > t) {
      this.fromInt(1)
    } else {
      for (
        this.fromNumber(t, r),
          this.testBit(t - 1) ||
            this.bitwiseTo(e.ONE.shiftLeft(t - 1), ht, this),
          this.isEven() && this.dAddOffset(1, 0);
        !this.isProbablePrime(i);

      ) {
        this.dAddOffset(2, 0)
        this.bitLength() > t && this.subTo(e.ONE.shiftLeft(t - 1), this)
      }
    }
  } else {
    var s = new Array(),
      n = 7 & t
    s.length = (t >> 3) + 1
    i.nextBytes(s)
    n > 0 ? (s[0] &= (1 << n) - 1) : (s[0] = 0)
    this.fromString(s, 256)
  }
}
function tt() {
  var t = this.t,
    e = new Array()
  e[0] = this.s
  var i,
    r = this.DB - ((t * this.DB) % 8),
    s = 0
  if (t-- > 0) {
    for (
      r < this.DB &&
      (i = this[t] >> r) != (this.s & this.DM) >> r &&
      (e[s++] = i | (this.s << (this.DB - r)));
      t >= 0;

    ) {
      8 > r
        ? ((i = (this[t] & ((1 << r) - 1)) << (8 - r)),
          (i |= this[--t] >> (r += this.DB - 8)))
        : ((i = (this[t] >> (r -= 8)) & 255), 0 >= r && ((r += this.DB), --t))
      0 != (128 & i) && (i |= -256)
      0 == s && (128 & this.s) != (128 & i) && ++s
      ;(s > 0 || i != this.s) && (e[s++] = i)
    }
  }
  return e
}
function et(t) {
  return 0 == this.compareTo(t)
}
function it(t) {
  return this.compareTo(t) < 0 ? this : t
}
function rt(t) {
  return this.compareTo(t) > 0 ? this : t
}
function st(t, e, i) {
  var r,
    s,
    n = Math.min(t.t, this.t)
  for (r = 0; n > r; ++r) {
    i[r] = e(this[r], t[r])
  }
  if (t.t < this.t) {
    for (s = t.s & this.DM, r = n; r < this.t; ++r) {
      i[r] = e(this[r], s)
    }
    i.t = this.t
  } else {
    for (s = this.s & this.DM, r = n; r < t.t; ++r) {
      i[r] = e(s, t[r])
    }
    i.t = t.t
  }
  i.s = e(this.s, t.s)
  i.clamp()
}
function nt(t, e) {
  return t & e
}
function ot(t) {
  var e = i()
  return this.bitwiseTo(t, nt, e), e
}
function ht(t, e) {
  return t | e
}
function at(t) {
  var e = i()
  return this.bitwiseTo(t, ht, e), e
}
function ut(t, e) {
  return t ^ e
}
function ct(t) {
  var e = i()
  return this.bitwiseTo(t, ut, e), e
}
function ft(t, e) {
  return t & ~e
}
function pt(t) {
  var e = i()
  return this.bitwiseTo(t, ft, e), e
}
function lt() {
  for (var t = i(), e = 0; e < this.t; ++e) {
    t[e] = this.DM & ~this[e]
  }
  return (t.t = this.t), (t.s = ~this.s), t
}
function dt(t) {
  var e = i()
  return 0 > t ? this.rShiftTo(-t, e) : this.lShiftTo(t, e), e
}
function gt(t) {
  var e = i()
  return 0 > t ? this.lShiftTo(-t, e) : this.rShiftTo(t, e), e
}
function mt(t) {
  if (0 == t) {
    return -1
  }
  var e = 0
  return (
    0 == (65535 & t) && ((t >>= 16), (e += 16)),
    0 == (255 & t) && ((t >>= 8), (e += 8)),
    0 == (15 & t) && ((t >>= 4), (e += 4)),
    0 == (3 & t) && ((t >>= 2), (e += 2)),
    0 == (1 & t) && ++e,
    e
  )
}
function yt() {
  for (var t = 0; t < this.t; ++t) {
    if (0 != this[t]) {
      return t * this.DB + mt(this[t])
    }
  }
  return this.s < 0 ? this.t * this.DB : -1
}
function vt(t) {
  for (var e = 0; 0 != t; ) {
    t &= t - 1
    ++e
  }
  return e
}
function bt() {
  for (var t = 0, e = this.s & this.DM, i = 0; i < this.t; ++i) {
    t += vt(this[i] ^ e)
  }
  return t
}
function Tt(t) {
  var e = Math.floor(t / this.DB)
  return e >= this.t ? 0 != this.s : 0 != (this[e] & (1 << t % this.DB))
}
function St(t, i) {
  var r = e.ONE.shiftLeft(t)
  return this.bitwiseTo(r, i, r), r
}
function Rt(t) {
  return this.changeBit(t, ht)
}
function Et(t) {
  return this.changeBit(t, ft)
}
function Dt(t) {
  return this.changeBit(t, ut)
}
function wt(t, e) {
  for (var i = 0, r = 0, s = Math.min(t.t, this.t); s > i; ) {
    r += this[i] + t[i]
    e[i++] = r & this.DM
    r >>= this.DB
  }
  if (t.t < this.t) {
    for (r += t.s; i < this.t; ) {
      r += this[i]
      e[i++] = r & this.DM
      r >>= this.DB
    }
    r += this.s
  } else {
    for (r += this.s; i < t.t; ) {
      r += t[i]
      e[i++] = r & this.DM
      r >>= this.DB
    }
    r += t.s
  }
  e.s = 0 > r ? -1 : 0
  r > 0 ? (e[i++] = r) : -1 > r && (e[i++] = this.DV + r)
  e.t = i
  e.clamp()
}
function xt(t) {
  var e = i()
  return this.addTo(t, e), e
}
function Bt(t) {
  var e = i()
  return this.subTo(t, e), e
}
function Kt(t) {
  var e = i()
  return this.multiplyTo(t, e), e
}
function At() {
  var t = i()
  return this.squareTo(t), t
}
function Ut(t) {
  var e = i()
  return this.divRemTo(t, e, null), e
}
function Ot(t) {
  var e = i()
  return this.divRemTo(t, null, e), e
}
function Vt(t) {
  var e = i(),
    r = i()
  return this.divRemTo(t, e, r), new Array(e, r)
}
function Nt(t) {
  this[this.t] = this.am(0, t - 1, this, 0, 0, this.t)
  ++this.t
  this.clamp()
}
function Jt(t, e) {
  if (0 != t) {
    for (; this.t <= e; ) {
      this[this.t++] = 0
    }
    for (this[e] += t; this[e] >= this.DV; ) {
      this[e] -= this.DV
      ++e >= this.t && (this[this.t++] = 0)
      ++this[e]
    }
  }
}
function It() {}
function Pt(t) {
  return t
}
function Mt(t, e, i) {
  t.multiplyTo(e, i)
}
function Lt(t, e) {
  t.squareTo(e)
}
function qt(t) {
  return this.exp(t, new It())
}
function Ct(t, e, i) {
  var r = Math.min(this.t + t.t, e)
  for (i.s = 0, i.t = r; r > 0; ) {
    i[--r] = 0
  }
  var s
  for (s = i.t - this.t; s > r; ++r) {
    i[r + this.t] = this.am(0, t[r], i, r, 0, this.t)
  }
  for (s = Math.min(t.t, e); s > r; ++r) {
    this.am(0, t[r], i, r, 0, e - r)
  }
  i.clamp()
}
function Ht(t, e, i) {
  --e
  var r = (i.t = this.t + t.t - e)
  for (i.s = 0; --r >= 0; ) {
    i[r] = 0
  }
  for (r = Math.max(e - this.t, 0); r < t.t; ++r) {
    i[this.t + r - e] = this.am(e - r, t[r], i, 0, 0, this.t + r - e)
  }
  i.clamp()
  i.drShiftTo(1, i)
}
function jt(t) {
  this.r2 = i()
  this.q3 = i()
  e.ONE.dlShiftTo(2 * t.t, this.r2)
  this.mu = this.r2.divide(t)
  this.m = t
}
function kt(t) {
  if (t.s < 0 || t.t > 2 * this.m.t) {
    return t.mod(this.m)
  }
  if (t.compareTo(this.m) < 0) {
    return t
  }
  var e = i()
  return t.copyTo(e), this.reduce(e), e
}
function Ft(t) {
  return t
}
function _t(t) {
  for (
    t.drShiftTo(this.m.t - 1, this.r2),
      t.t > this.m.t + 1 && ((t.t = this.m.t + 1), t.clamp()),
      this.mu.multiplyUpperTo(this.r2, this.m.t + 1, this.q3),
      this.m.multiplyLowerTo(this.q3, this.m.t + 1, this.r2);
    t.compareTo(this.r2) < 0;

  ) {
    t.dAddOffset(1, this.m.t + 1)
  }
  for (t.subTo(this.r2, t); t.compareTo(this.m) >= 0; ) {
    t.subTo(this.m, t)
  }
}
function zt(t, e) {
  t.squareTo(e)
  this.reduce(e)
}
function Zt(t, e, i) {
  t.multiplyTo(e, i)
  this.reduce(i)
}
function Gt(t, e) {
  var r,
    s,
    n = t.bitLength(),
    o = c(1)
  if (0 >= n) {
    return o
  }
  r = 18 > n ? 1 : 48 > n ? 3 : 144 > n ? 4 : 768 > n ? 5 : 6
  s = 8 > n ? new A(e) : e.isEven() ? new jt(e) : new P(e)
  var h = new Array(),
    a = 3,
    u = r - 1,
    f = (1 << r) - 1
  if (((h[1] = s.convert(this)), r > 1)) {
    var p = i()
    for (s.sqrTo(h[1], p); f >= a; ) {
      h[a] = i()
      s.mulTo(p, h[a - 2], h[a])
      a += 2
    }
  }
  var l,
    d,
    g = t.t - 1,
    m = true,
    v = i()
  for (n = y(t[g]) - 1; g >= 0; ) {
    for (
      n >= u
        ? (l = (t[g] >> (n - u)) & f)
        : ((l = (t[g] & ((1 << (n + 1)) - 1)) << (u - n)),
          g > 0 && (l |= t[g - 1] >> (this.DB + n - u))),
        a = r;
      0 == (1 & l);

    ) {
      l >>= 1
      --a
    }
    if (((n -= a) < 0 && ((n += this.DB), --g), m)) {
      h[l].copyTo(o)
      m = false
    } else {
      for (; a > 1; ) {
        s.sqrTo(o, v)
        s.sqrTo(v, o)
        a -= 2
      }
      a > 0 ? s.sqrTo(o, v) : ((d = o), (o = v), (v = d))
      s.mulTo(v, h[l], o)
    }
    for (; g >= 0 && 0 == (t[g] & (1 << n)); ) {
      s.sqrTo(o, v)
      d = o
      o = v
      v = d
      --n < 0 && ((n = this.DB - 1), --g)
    }
  }
  return s.revert(o)
}
function $t(t) {
  var e = this.s < 0 ? this.negate() : this.clone(),
    i = t.s < 0 ? t.negate() : t.clone()
  if (e.compareTo(i) < 0) {
    var r = e
    e = i
    i = r
  }
  var s = e.getLowestSetBit(),
    n = i.getLowestSetBit()
  if (0 > n) {
    return e
  }
  for (
    n > s && (n = s), n > 0 && (e.rShiftTo(n, e), i.rShiftTo(n, i));
    e.signum() > 0;

  ) {
    ;(s = e.getLowestSetBit()) > 0 && e.rShiftTo(s, e)
    ;(s = i.getLowestSetBit()) > 0 && i.rShiftTo(s, i)
    e.compareTo(i) >= 0
      ? (e.subTo(i, e), e.rShiftTo(1, e))
      : (i.subTo(e, i), i.rShiftTo(1, i))
  }
  return n > 0 && i.lShiftTo(n, i), i
}
function Yt(t) {
  if (0 >= t) {
    return 0
  }
  var e = this.DV % t,
    i = this.s < 0 ? t - 1 : 0
  if (this.t > 0) {
    if (0 == e) {
      i = this[0] % t
    } else {
      for (var r = this.t - 1; r >= 0; --r) {
        i = (e * i + this[r]) % t
      }
    }
  }
  return i
}
function Wt(t) {
  var i = t.isEven()
  if ((this.isEven() && i) || 0 == t.signum()) {
    return e.ZERO
  }
  for (
    var r = t.clone(), s = this.clone(), n = c(1), o = c(0), h = c(0), a = c(1);
    0 != r.signum();

  ) {
    for (; r.isEven(); ) {
      r.rShiftTo(1, r)
      i
        ? ((n.isEven() && o.isEven()) || (n.addTo(this, n), o.subTo(t, o)),
          n.rShiftTo(1, n))
        : o.isEven() || o.subTo(t, o)
      o.rShiftTo(1, o)
    }
    for (; s.isEven(); ) {
      s.rShiftTo(1, s)
      i
        ? ((h.isEven() && a.isEven()) || (h.addTo(this, h), a.subTo(t, a)),
          h.rShiftTo(1, h))
        : a.isEven() || a.subTo(t, a)
      a.rShiftTo(1, a)
    }
    r.compareTo(s) >= 0
      ? (r.subTo(s, r), i && n.subTo(h, n), o.subTo(a, o))
      : (s.subTo(r, s), i && h.subTo(n, h), a.subTo(o, a))
  }
  return 0 != s.compareTo(e.ONE)
    ? e.ZERO
    : a.compareTo(t) >= 0
    ? a.subtract(t)
    : a.signum() < 0
    ? (a.addTo(t, a), a.signum() < 0 ? a.add(t) : a)
    : a
}
function Qt(t) {
  var e,
    i = this.abs()
  if (1 == i.t && i[0] <= Ae[Ae.length - 1]) {
    for (e = 0; e < Ae.length; ++e) {
      if (i[0] == Ae[e]) {
        return true
      }
    }
    return false
  }
  if (i.isEven()) {
    return false
  }
  for (e = 1; e < Ae.length; ) {
    for (var r = Ae[e], s = e + 1; s < Ae.length && Ue > r; ) {
      r *= Ae[s++]
    }
    for (r = i.modInt(r); s > e; ) {
      if (r % Ae[e++] == 0) {
        return false
      }
    }
  }
  return i.millerRabin(t)
}
function Xt(t) {
  var r = this.subtract(e.ONE),
    s = r.getLowestSetBit()
  if (0 >= s) {
    return false
  }
  var n = r.shiftRight(s)
  t = (t + 1) >> 1
  t > Ae.length && (t = Ae.length)
  for (var o = i(), h = 0; t > h; ++h) {
    o.fromInt(Ae[Math.floor(Math.random() * Ae.length)])
    var a = o.modPow(n, this)
    if (0 != a.compareTo(e.ONE) && 0 != a.compareTo(r)) {
      for (var u = 1; u++ < s && 0 != a.compareTo(r); ) {
        if (((a = a.modPowInt(2, this)), 0 == a.compareTo(e.ONE))) {
          return false
        }
      }
      if (0 != a.compareTo(r)) {
        return false
      }
    }
  }
  return true
}
function te() {
  this.i = 0
  this.j = 0
  this.S = new Array()
}
function ee(t) {
  var e, i, r
  for (e = 0; 256 > e; ++e) {
    this.S[e] = e
  }
  for (i = 0, e = 0; 256 > e; ++e) {
    i = (i + this.S[e] + t[e % t.length]) & 255
    r = this.S[e]
    this.S[e] = this.S[i]
    this.S[i] = r
  }
  this.i = 0
  this.j = 0
}
function ie() {
  var t
  return (
    (this.i = (this.i + 1) & 255),
    (this.j = (this.j + this.S[this.i]) & 255),
    (t = this.S[this.i]),
    (this.S[this.i] = this.S[this.j]),
    (this.S[this.j] = t),
    this.S[(t + this.S[this.i]) & 255]
  )
}
function re() {
  return new te()
}
function se() {
  if (null == Oe) {
    for (Oe = re(); Je > Ne; ) {
      var t = Math.floor(65536 * Math.random())
      Ve[Ne++] = 255 & t
    }
    for (Oe.init(Ve), Ne = 0; Ne < Ve.length; ++Ne) {
      Ve[Ne] = 0
    }
    Ne = 0
  }
  return Oe.next()
}
function ne(t) {
  var e
  for (e = 0; e < t.length; ++e) {
    t[e] = se()
  }
}
function oe() {}
function he(t, i) {
  return new e(t, i)
}
function ae(t, i) {
  if (i < t.length + 11) {
    return console.error('Message too long for RSA'), null
  }
  for (var r = new Array(), s = t.length - 1; s >= 0 && i > 0; ) {
    var n = t.charCodeAt(s--)
    128 > n
      ? (r[--i] = n)
      : n > 127 && 2048 > n
      ? ((r[--i] = (63 & n) | 128), (r[--i] = (n >> 6) | 192))
      : ((r[--i] = (63 & n) | 128),
        (r[--i] = ((n >> 6) & 63) | 128),
        (r[--i] = (n >> 12) | 224))
  }
  r[--i] = 0
  for (var o = new oe(), h = new Array(); i > 2; ) {
    for (h[0] = 0; 0 == h[0]; ) {
      o.nextBytes(h)
    }
    r[--i] = h[0]
  }
  return (r[--i] = 2), (r[--i] = 0), new e(r)
}
function ue() {
  this.n = null
  this.e = 0
  this.d = null
  this.p = null
  this.q = null
  this.dmp1 = null
  this.dmq1 = null
  this.coeff = null
}
function ce(t, e) {
  null != t && null != e && t.length > 0 && e.length > 0
    ? ((this.n = he(t, 16)), (this.e = parseInt(e, 16)))
    : console.error('Invalid RSA public key')
}
function fe(t) {
  return t.modPowInt(this.e, this.n)
}
function pe(t) {
  var e = ae(t, (this.n.bitLength() + 7) >> 3)
  if (null == e) {
    return null
  }
  var i = this.doPublic(e)
  if (null == i) {
    return null
  }
  var r = i.toString(16)
  return 0 == (1 & r.length) ? r : '0' + r
}
function le(t, e) {
  for (var i = t.toByteArray(), r = 0; r < i.length && 0 == i[r]; ) {
    ++r
  }
  if (i.length - r != e - 1 || 2 != i[r]) {
    return null
  }
  for (++r; 0 != i[r]; ) {
    if (++r >= i.length) {
      return null
    }
  }
  for (var s = ''; ++r < i.length; ) {
    var n = 255 & i[r]
    128 > n
      ? (s += String.fromCharCode(n))
      : n > 191 && 224 > n
      ? ((s += String.fromCharCode(((31 & n) << 6) | (63 & i[r + 1]))), ++r)
      : ((s += String.fromCharCode(
          ((15 & n) << 12) | ((63 & i[r + 1]) << 6) | (63 & i[r + 2])
        )),
        (r += 2))
  }
  return s
}
function de(t, e, i) {
  null != t && null != e && t.length > 0 && e.length > 0
    ? ((this.n = he(t, 16)), (this.e = parseInt(e, 16)), (this.d = he(i, 16)))
    : console.error('Invalid RSA private key')
}
function ge(t, e, i, r, s, n, o, h) {
  null != t && null != e && t.length > 0 && e.length > 0
    ? ((this.n = he(t, 16)),
      (this.e = parseInt(e, 16)),
      (this.d = he(i, 16)),
      (this.p = he(r, 16)),
      (this.q = he(s, 16)),
      (this.dmp1 = he(n, 16)),
      (this.dmq1 = he(o, 16)),
      (this.coeff = he(h, 16)))
    : console.error('Invalid RSA private key')
}
function me(t, i) {
  var r = new oe(),
    s = t >> 1
  this.e = parseInt(i, 16)
  for (var n = new e(i, 16); ; ) {
    for (
      ;
      (this.p = new e(t - s, 1, r)),
        0 != this.p.subtract(e.ONE).gcd(n).compareTo(e.ONE) ||
          !this.p.isProbablePrime(10);

    ) {}
    for (
      ;
      (this.q = new e(s, 1, r)),
        0 != this.q.subtract(e.ONE).gcd(n).compareTo(e.ONE) ||
          !this.q.isProbablePrime(10);

    ) {}
    if (this.p.compareTo(this.q) <= 0) {
      var o = this.p
      this.p = this.q
      this.q = o
    }
    var h = this.p.subtract(e.ONE),
      a = this.q.subtract(e.ONE),
      u = h.multiply(a)
    if (0 == u.gcd(n).compareTo(e.ONE)) {
      this.n = this.p.multiply(this.q)
      this.d = n.modInverse(u)
      this.dmp1 = this.d.mod(h)
      this.dmq1 = this.d.mod(a)
      this.coeff = this.q.modInverse(this.p)
      break
    }
  }
}
function ye(t) {
  if (null == this.p || null == this.q) {
    return t.modPow(this.d, this.n)
  }
  for (
    var e = t.mod(this.p).modPow(this.dmp1, this.p),
      i = t.mod(this.q).modPow(this.dmq1, this.q);
    e.compareTo(i) < 0;

  ) {
    e = e.add(this.p)
  }
  return e.subtract(i).multiply(this.coeff).mod(this.p).multiply(this.q).add(i)
}
function ve(t) {
  var e = he(t, 16),
    i = this.doPrivate(e)
  return null == i ? null : le(i, (this.n.bitLength() + 7) >> 3)
}
function be(t) {
  var e,
    i,
    r = ''
  for (e = 0; e + 3 <= t.length; e += 3) {
    i = parseInt(t.substring(e, e + 3), 16)
    r += Le.charAt(i >> 6) + Le.charAt(63 & i)
  }
  for (
    e + 1 == t.length
      ? ((i = parseInt(t.substring(e, e + 1), 16)), (r += Le.charAt(i << 2)))
      : e + 2 == t.length &&
        ((i = parseInt(t.substring(e, e + 2), 16)),
        (r += Le.charAt(i >> 2) + Le.charAt((3 & i) << 4)));
    (3 & r.length) > 0;

  ) {
    r += qe
  }
  return r
}
function Te(t) {
  var e,
    i,
    r = '',
    s = 0
  for (e = 0; e < t.length && t.charAt(e) != qe; ++e) {
    v = Le.indexOf(t.charAt(e))
    v < 0 ||
      (0 == s
        ? ((r += o(v >> 2)), (i = 3 & v), (s = 1))
        : 1 == s
        ? ((r += o((i << 2) | (v >> 4))), (i = 15 & v), (s = 2))
        : 2 == s
        ? ((r += o(i)), (r += o(v >> 2)), (i = 3 & v), (s = 3))
        : ((r += o((i << 2) | (v >> 4))), (r += o(15 & v)), (s = 0)))
  }
  return 1 == s && (r += o(i << 2)), r
}
var Se,
  Re = 244837814094590,
  Ee = 15715070 == (16777215 & Re)
Ee && 'Microsoft Internet Explorer' == "navigator.appName"
  ? ((e.prototype.am = s), (Se = 30))
  : Ee && 'Netscape' != "navigator.appName"
  ? ((e.prototype.am = r), (Se = 26))
  : ((e.prototype.am = n), (Se = 28))
e.prototype.DB = Se
e.prototype.DM = (1 << Se) - 1
e.prototype.DV = 1 << Se
var De = 52
e.prototype.FV = Math.pow(2, De)
e.prototype.F1 = De - Se
e.prototype.F2 = 2 * Se - De
var we,
  xe,
  Be = '0123456789abcdefghijklmnopqrstuvwxyz',
  Ke = new Array()
for (we = '0'.charCodeAt(0), xe = 0; 9 >= xe; ++xe) {
  Ke[we++] = xe
}
for (we = 'a'.charCodeAt(0), xe = 10; 36 > xe; ++xe) {
  Ke[we++] = xe
}
for (we = 'A'.charCodeAt(0), xe = 10; 36 > xe; ++xe) {
  Ke[we++] = xe
}
A.prototype.convert = U
A.prototype.revert = O
A.prototype.reduce = V
A.prototype.mulTo = N
A.prototype.sqrTo = J
P.prototype.convert = M
P.prototype.revert = L
P.prototype.reduce = q
P.prototype.mulTo = H
P.prototype.sqrTo = C
e.prototype.copyTo = a
e.prototype.fromInt = u
e.prototype.fromString = f
e.prototype.clamp = p
e.prototype.dlShiftTo = T
e.prototype.drShiftTo = S
e.prototype.lShiftTo = R
e.prototype.rShiftTo = E
e.prototype.subTo = D
e.prototype.multiplyTo = w
e.prototype.squareTo = x
e.prototype.divRemTo = B
e.prototype.invDigit = I
e.prototype.isEven = j
e.prototype.exp = k
e.prototype.toString = l
e.prototype.negate = d
e.prototype.abs = g
e.prototype.compareTo = m
e.prototype.bitLength = b
e.prototype.mod = K
e.prototype.modPowInt = F
e.ZERO = c(0)
e.ONE = c(1)
It.prototype.convert = Pt
It.prototype.revert = Pt
It.prototype.mulTo = Mt
It.prototype.sqrTo = Lt
jt.prototype.convert = kt
jt.prototype.revert = Ft
jt.prototype.reduce = _t
jt.prototype.mulTo = Zt
jt.prototype.sqrTo = zt
var Ae = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
    421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
    509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
    613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
    821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
    919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997,
  ],
  Ue = (1 << 26) / Ae[Ae.length - 1]
e.prototype.chunkSize = $
e.prototype.toRadix = W
e.prototype.fromRadix = Q
e.prototype.fromNumber = X
e.prototype.bitwiseTo = st
e.prototype.changeBit = St
e.prototype.addTo = wt
e.prototype.dMultiply = Nt
e.prototype.dAddOffset = Jt
e.prototype.multiplyLowerTo = Ct
e.prototype.multiplyUpperTo = Ht
e.prototype.modInt = Yt
e.prototype.millerRabin = Xt
e.prototype.clone = _
e.prototype.intValue = z
e.prototype.byteValue = Z
e.prototype.shortValue = G
e.prototype.signum = Y
e.prototype.toByteArray = tt
e.prototype.equals = et
e.prototype.min = it
e.prototype.max = rt
e.prototype.and = ot
e.prototype.or = at
e.prototype.xor = ct
e.prototype.andNot = pt
e.prototype.not = lt
e.prototype.shiftLeft = dt
e.prototype.shiftRight = gt
e.prototype.getLowestSetBit = yt
e.prototype.bitCount = bt
e.prototype.testBit = Tt
e.prototype.setBit = Rt
e.prototype.clearBit = Et
e.prototype.flipBit = Dt
e.prototype.add = xt
e.prototype.subtract = Bt
e.prototype.multiply = Kt
e.prototype.divide = Ut
e.prototype.remainder = Ot
e.prototype.divideAndRemainder = Vt
e.prototype.modPow = Gt
e.prototype.modInverse = Wt
e.prototype.pow = qt
e.prototype.gcd = $t
e.prototype.isProbablePrime = Qt
e.prototype.square = At
te.prototype.init = ee
te.prototype.next = ie
var Oe,
  Ve,
  Ne,
  Je = 256
if (null == Ve) {
  Ve = new Array()
  Ne = 0
  var Ie

    var Pe = new Uint32Array(256)
    for (getRandomValues(Pe), Ie = 0; Ie < Pe.length; ++Ie) {
      Ve[Ne++] = 255 & Pe[Ie]
    }


}
oe.prototype.nextBytes = ne
ue.prototype.doPublic = fe
ue.prototype.setPublic = ce
ue.prototype.encrypt = pe
ue.prototype.doPrivate = ye
ue.prototype.setPrivate = de
ue.prototype.setPrivateEx = ge
ue.prototype.generate = me
ue.prototype.decrypt = ve
;(function () {
  var t = function (t, r, s) {
    var n = new oe(),
      o = t >> 1
    this.e = parseInt(r, 16)
    var h = new e(r, 16),
      a = this,
      u = function () {
        var r = function () {
            if (a.p.compareTo(a.q) <= 0) {
              var t = a.p
              a.p = a.q
              a.q = t
            }
            var i = a.p.subtract(e.ONE),
              r = a.q.subtract(e.ONE),
              n = i.multiply(r)
            0 == n.gcd(h).compareTo(e.ONE)
              ? ((a.n = a.p.multiply(a.q)),
                (a.d = h.modInverse(n)),
                (a.dmp1 = a.d.mod(i)),
                (a.dmq1 = a.d.mod(r)),
                (a.coeff = a.q.modInverse(a.p)),
                setTimeout(function () {
                  s()
                }, 0))
              : setTimeout(u, 0)
          },
          c = function () {
            a.q = i()
            a.q.fromNumberAsync(o, 1, n, function () {
              a.q.subtract(e.ONE).gcda(h, function (t) {
                0 == t.compareTo(e.ONE) && a.q.isProbablePrime(10)
                  ? setTimeout(r, 0)
                  : setTimeout(c, 0)
              })
            })
          },
          f = function () {
            a.p = i()
            a.p.fromNumberAsync(t - o, 1, n, function () {
              a.p.subtract(e.ONE).gcda(h, function (t) {
                0 == t.compareTo(e.ONE) && a.p.isProbablePrime(10)
                  ? setTimeout(c, 0)
                  : setTimeout(f, 0)
              })
            })
          }
        setTimeout(f, 0)
      }
    setTimeout(u, 0)
  }
  ue.prototype.generateAsync = t
  var r = function (t, e) {
    var i = this.s < 0 ? this.negate() : this.clone(),
      r = t.s < 0 ? t.negate() : t.clone()
    if (i.compareTo(r) < 0) {
      var s = i
      i = r
      r = s
    }
    var n = i.getLowestSetBit(),
      o = r.getLowestSetBit()
    if (0 > o) {
      return void e(i)
    }
    o > n && (o = n)
    o > 0 && (i.rShiftTo(o, i), r.rShiftTo(o, r))
    var h = function () {
      ;(n = i.getLowestSetBit()) > 0 && i.rShiftTo(n, i)
      ;(n = r.getLowestSetBit()) > 0 && r.rShiftTo(n, r)
      i.compareTo(r) >= 0
        ? (i.subTo(r, i), i.rShiftTo(1, i))
        : (r.subTo(i, r), r.rShiftTo(1, r))
      i.signum() > 0
        ? setTimeout(h, 0)
        : (o > 0 && r.lShiftTo(o, r),
          setTimeout(function () {
            e(r)
          }, 0))
    }
    setTimeout(h, 10)
  }
  e.prototype.gcda = r
  var s = function (t, i, r, s) {
    if ('number' == typeof i) {
      if (2 > t) {
        this.fromInt(1)
      } else {
        this.fromNumber(t, r)
        this.testBit(t - 1) || this.bitwiseTo(e.ONE.shiftLeft(t - 1), ht, this)
        this.isEven() && this.dAddOffset(1, 0)
        var n = this,
          o = function () {
            n.dAddOffset(2, 0)
            n.bitLength() > t && n.subTo(e.ONE.shiftLeft(t - 1), n)
            n.isProbablePrime(i)
              ? setTimeout(function () {
                  s()
                }, 0)
              : setTimeout(o, 0)
          }
        setTimeout(o, 0)
      }
    } else {
      var h = new Array(),
        a = 7 & t
      h.length = (t >> 3) + 1
      i.nextBytes(h)
      a > 0 ? (h[0] &= (1 << a) - 1) : (h[0] = 0)
      this.fromString(h, 256)
    }
  }
  e.prototype.fromNumberAsync = s
})()
var Le = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
  qe = '=',
  Ce = Ce || {}
Ce.env = Ce.env || {}
var He = Ce,
  je = Object.prototype,
  ke = '[object Function]',
  Fe = ['toString', 'valueOf']


Ce.isFunction = function (t) {
  return 'function' == typeof t || je.toString.apply(t) === ke
}
Ce._IEEnumFix = function () {}
Ce.extend = function (t, e, i) {
  if (!e || !t) {
    throw new Error(
      'extend failed, please check that all dependencies are included.'
    )
  }
  var r,
    s = function () {}
  if (
    ((s.prototype = e.prototype),
    (t.prototype = new s()),
    (t.prototype.constructor = t),
    (t.superclass = e.prototype),
    e.prototype.constructor == je.constructor && (e.prototype.constructor = e),
    i)
  ) {
    for (r in i) He.hasOwnProperty(i, r) && (t.prototype[r] = i[r])
    He._IEEnumFix(t.prototype, i)
  }
}
;('undefined' != typeof KJUR && KJUR) || (KJUR = {})
;('undefined' != typeof KJUR.asn1 && KJUR.asn1) || (KJUR.asn1 = {})
KJUR.asn1.ASN1Util = new (function () {
  this.integerToByteHex = function (t) {
    var e = t.toString(16)
    return e.length % 2 == 1 && (e = '0' + e), e
  }
  this.bigIntToMinTwosComplementsHex = function (t) {
    var i = t.toString(16)
    if ('-' != i.substr(0, 1)) {
      i.length % 2 == 1 ? (i = '0' + i) : i.match(/^[0-7]/) || (i = '00' + i)
    } else {
      var r = i.substr(1),
        s = r.length
      s % 2 == 1 ? (s += 1) : i.match(/^[0-7]/) || (s += 2)
      for (var n = '', o = 0; s > o; o++) {
        n += 'f'
      }
      var h = new e(n, 16),
        a = h.xor(t).add(e.ONE)
      i = a.toString(16).replace(/^-/, '')
    }
    return i
  }
  this.getPEMStringFromHex = function (t, e) {
    var i = CryptoJS.enc.Hex.parse(t),
      r = CryptoJS.enc.Base64.stringify(i),
      s = r.replace(/(.{64})/g, '$1\\r\\n')
    return (
      (s = s.replace(/\\r\\n$/, '')),
      '-----BEGIN ' + e + '-----\\r\\n' + s + '\\r\\n-----END ' + e + '-----\\r\\n'
    )
  }
})()
KJUR.asn1.ASN1Object = function () {
  this.getLengthHexFromValue = function () {
    if ('undefined' == typeof this.hV || null == this.hV) {
      throw 'this.hV is null or undefined.'
    }
    if (this.hV.length % 2 == 1) {
      throw 'value hex must be even length: n=' + ''.length + ',v=' + this.hV
    }
    var e = this.hV.length / 2,
      i = e.toString(16)
    if ((i.length % 2 == 1 && (i = '0' + i), 128 > e)) {
      return i
    }
    var r = i.length / 2
    if (r > 15) {
      throw 'ASN.1 length too long to represent by 8x: n = ' + e.toString(16)
    }
    var s = 128 + r
    return s.toString(16) + i
  }
  this.getEncodedHex = function () {
    return (
      (null == this.hTLV || this.isModified) &&
        ((this.hV = this.getFreshValueHex()),
        (this.hL = this.getLengthHexFromValue()),
        (this.hTLV = this.hT + this.hL + this.hV),
        (this.isModified = false)),
      this.hTLV
    )
  }
  this.getValueHex = function () {
    return this.getEncodedHex(), this.hV
  }
  this.getFreshValueHex = function () {
    return ''
  }
}
KJUR.asn1.DERAbstractString = function (t) {
  KJUR.asn1.DERAbstractString.superclass.constructor.call(this)
  this.getString = function () {
    return this.s
  }
  this.setString = function (t) {
    this.hTLV = null
    this.isModified = true
    this.s = t
    this.hV = stohex(this.s)
  }
  this.setStringHex = function (t) {
    this.hTLV = null
    this.isModified = true
    this.s = null
    this.hV = t
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.str
      ? this.setString(t.str)
      : 'undefined' != typeof t.hex && this.setStringHex(t.hex))
}
Ce.extend(KJUR.asn1.DERAbstractString, KJUR.asn1.ASN1Object)
KJUR.asn1.DERAbstractTime = function (t) {
  KJUR.asn1.DERAbstractTime.superclass.constructor.call(this)
  this.localDateToUTC = function (t) {
    utc = t.getTime() + 60000 * t.getTimezoneOffset()
    var e = new Date(utc)
    return e
  }
  this.formatDate = function (t, e) {
    var i = this.zeroPadding,
      r = this.localDateToUTC(t),
      s = String(r.getFullYear())
    'utc' == e && (s = s.substr(2, 2))
    var n = i(String(r.getMonth() + 1), 2),
      o = i(String(r.getDate()), 2),
      h = i(String(r.getHours()), 2),
      a = i(String(r.getMinutes()), 2),
      u = i(String(r.getSeconds()), 2)
    return s + n + o + h + a + u + 'Z'
  }
  this.zeroPadding = function (t, e) {
    return t.length >= e ? t : new Array(e - t.length + 1).join('0') + t
  }
  this.getString = function () {
    return this.s
  }
  this.setString = function (t) {
    this.hTLV = null
    this.isModified = true
    this.s = t
    this.hV = stohex(this.s)
  }
  this.setByDateValue = function (t, e, i, r, s, n) {
    var o = new Date(Date.UTC(t, e - 1, i, r, s, n, 0))
    this.setByDate(o)
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
}
Ce.extend(KJUR.asn1.DERAbstractTime, KJUR.asn1.ASN1Object)
KJUR.asn1.DERAbstractStructured = function (t) {
  KJUR.asn1.DERAbstractString.superclass.constructor.call(this)
  this.setByASN1ObjectArray = function (t) {
    this.hTLV = null
    this.isModified = true
    this.asn1Array = t
  }
  this.appendASN1Object = function (t) {
    this.hTLV = null
    this.isModified = true
    this.asn1Array.push(t)
  }
  this.asn1Array = new Array()
  'undefined' != typeof t &&
    'undefined' != typeof t.array &&
    (this.asn1Array = t.array)
}
Ce.extend(KJUR.asn1.DERAbstractStructured, KJUR.asn1.ASN1Object)
KJUR.asn1.DERBoolean = function () {
  KJUR.asn1.DERBoolean.superclass.constructor.call(this)
  this.hT = '01'
  this.hTLV = '0101ff'
}
Ce.extend(KJUR.asn1.DERBoolean, KJUR.asn1.ASN1Object)
KJUR.asn1.DERInteger = function (t) {
  KJUR.asn1.DERInteger.superclass.constructor.call(this)
  this.hT = '02'
  this.setByBigInteger = function (t) {
    this.hTLV = null
    this.isModified = true
    this.hV = KJUR.asn1.ASN1Util.bigIntToMinTwosComplementsHex(t)
  }
  this.setByInteger = function (t) {
    var i = new e(String(t), 10)
    this.setByBigInteger(i)
  }
  this.setValueHex = function (t) {
    this.hV = t
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.bigint
      ? this.setByBigInteger(t.bigint)
      : 'undefined' != typeof t.int
      ? this.setByInteger(t.int)
      : 'undefined' != typeof t.hex && this.setValueHex(t.hex))
}
Ce.extend(KJUR.asn1.DERInteger, KJUR.asn1.ASN1Object)
KJUR.asn1.DERBitString = function (t) {
  KJUR.asn1.DERBitString.superclass.constructor.call(this)
  this.hT = '03'
  this.setHexValueIncludingUnusedBits = function (t) {
    this.hTLV = null
    this.isModified = true
    this.hV = t
  }
  this.setUnusedBitsAndHexValue = function (t, e) {
    if (0 > t || t > 7) {
      throw 'unused bits shall be from 0 to 7: u = ' + t
    }
    var i = '0' + t
    this.hTLV = null
    this.isModified = true
    this.hV = i + e
  }
  this.setByBinaryString = function (t) {
    t = t.replace(/0+$/, '')
    var e = 8 - (t.length % 8)
    8 == e && (e = 0)
    for (var i = 0; e >= i; i++) {
      t += '0'
    }
    for (var r = '', i = 0; i < t.length - 1; i += 8) {
      var s = t.substr(i, 8),
        n = parseInt(s, 2).toString(16)
      1 == n.length && (n = '0' + n)
      r += n
    }
    this.hTLV = null
    this.isModified = true
    this.hV = '0' + e + r
  }
  this.setByBooleanArray = function (t) {
    for (var e = '', i = 0; i < t.length; i++) {
      e += 1 == t[i] ? '1' : '0'
    }
    this.setByBinaryString(e)
  }
  this.newFalseArray = function (t) {
    for (var e = new Array(t), i = 0; t > i; i++) {
      e[i] = false
    }
    return e
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.hex
      ? this.setHexValueIncludingUnusedBits(t.hex)
      : 'undefined' != typeof t.bin
      ? this.setByBinaryString(t.bin)
      : 'undefined' != typeof t.array && this.setByBooleanArray(t.array))
}
Ce.extend(KJUR.asn1.DERBitString, KJUR.asn1.ASN1Object)
KJUR.asn1.DEROctetString = function (t) {
  KJUR.asn1.DEROctetString.superclass.constructor.call(this, t)
  this.hT = '04'
}
Ce.extend(KJUR.asn1.DEROctetString, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERNull = function () {
  KJUR.asn1.DERNull.superclass.constructor.call(this)
  this.hT = '05'
  this.hTLV = '0500'
}
Ce.extend(KJUR.asn1.DERNull, KJUR.asn1.ASN1Object)
KJUR.asn1.DERObjectIdentifier = function (t) {
  var i = function (t) {
      var e = t.toString(16)
      return 1 == e.length && (e = '0' + e), e
    },
    r = function (t) {
      var r = '',
        s = new e(t, 10),
        n = s.toString(2),
        o = 7 - (n.length % 7)
      7 == o && (o = 0)
      for (var h = '', a = 0; o > a; a++) {
        h += '0'
      }
      n = h + n
      for (var a = 0; a < n.length - 1; a += 7) {
        var u = n.substr(a, 7)
        a != n.length - 7 && (u = '1' + u)
        r += i(parseInt(u, 2))
      }
      return r
    }
  KJUR.asn1.DERObjectIdentifier.superclass.constructor.call(this)
  this.hT = '06'
  this.setValueHex = function (t) {
    this.hTLV = null
    this.isModified = true
    this.s = null
    this.hV = t
  }
  this.setValueOidString = function (t) {
    if (!t.match(/^[0-9.]+$/)) {
      throw 'malformed oid string: ' + t
    }
    var e = '',
      s = t.split('.'),
      n = 40 * parseInt(s[0]) + parseInt(s[1])
    e += i(n)
    s.splice(0, 2)
    for (var o = 0; o < s.length; o++) {
      e += r(s[o])
    }
    this.hTLV = null
    this.isModified = true
    this.s = null
    this.hV = e
  }
  this.setValueName = function (t) {
    if ('undefined' == typeof KJUR.asn1.x509.OID.name2oidList[t]) {
      throw 'DERObjectIdentifier oidName undefined: ' + t
    }
    var e = KJUR.asn1.x509.OID.name2oidList[t]
    this.setValueOidString(e)
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.oid
      ? this.setValueOidString(t.oid)
      : 'undefined' != typeof t.hex
      ? this.setValueHex(t.hex)
      : 'undefined' != typeof t.name && this.setValueName(t.name))
}
Ce.extend(KJUR.asn1.DERObjectIdentifier, KJUR.asn1.ASN1Object)
KJUR.asn1.DERUTF8String = function (t) {
  KJUR.asn1.DERUTF8String.superclass.constructor.call(this, t)
  this.hT = '0c'
}
Ce.extend(KJUR.asn1.DERUTF8String, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERNumericString = function (t) {
  KJUR.asn1.DERNumericString.superclass.constructor.call(this, t)
  this.hT = '12'
}
Ce.extend(KJUR.asn1.DERNumericString, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERPrintableString = function (t) {
  KJUR.asn1.DERPrintableString.superclass.constructor.call(this, t)
  this.hT = '13'
}
Ce.extend(KJUR.asn1.DERPrintableString, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERTeletexString = function (t) {
  KJUR.asn1.DERTeletexString.superclass.constructor.call(this, t)
  this.hT = '14'
}
Ce.extend(KJUR.asn1.DERTeletexString, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERIA5String = function (t) {
  KJUR.asn1.DERIA5String.superclass.constructor.call(this, t)
  this.hT = '16'
}
Ce.extend(KJUR.asn1.DERIA5String, KJUR.asn1.DERAbstractString)
KJUR.asn1.DERUTCTime = function (t) {
  KJUR.asn1.DERUTCTime.superclass.constructor.call(this, t)
  this.hT = '17'
  this.setByDate = function (t) {
    this.hTLV = null
    this.isModified = true
    this.date = t
    this.s = this.formatDate(this.date, 'utc')
    this.hV = stohex(this.s)
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.str
      ? this.setString(t.str)
      : 'undefined' != typeof t.hex
      ? this.setStringHex(t.hex)
      : 'undefined' != typeof t.date && this.setByDate(t.date))
}
Ce.extend(KJUR.asn1.DERUTCTime, KJUR.asn1.DERAbstractTime)
KJUR.asn1.DERGeneralizedTime = function (t) {
  KJUR.asn1.DERGeneralizedTime.superclass.constructor.call(this, t)
  this.hT = '18'
  this.setByDate = function (t) {
    this.hTLV = null
    this.isModified = true
    this.date = t
    this.s = this.formatDate(this.date, 'gen')
    this.hV = stohex(this.s)
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.str
      ? this.setString(t.str)
      : 'undefined' != typeof t.hex
      ? this.setStringHex(t.hex)
      : 'undefined' != typeof t.date && this.setByDate(t.date))
}
Ce.extend(KJUR.asn1.DERGeneralizedTime, KJUR.asn1.DERAbstractTime)
KJUR.asn1.DERSequence = function (t) {
  KJUR.asn1.DERSequence.superclass.constructor.call(this, t)
  this.hT = '30'
  this.getFreshValueHex = function () {
    for (var t = '', e = 0; e < this.asn1Array.length; e++) {
      var i = this.asn1Array[e]
      t += i.getEncodedHex()
    }
    return (this.hV = t), this.hV
  }
}
Ce.extend(KJUR.asn1.DERSequence, KJUR.asn1.DERAbstractStructured)
KJUR.asn1.DERSet = function (t) {
  KJUR.asn1.DERSet.superclass.constructor.call(this, t)
  this.hT = '31'
  this.getFreshValueHex = function () {
    for (var t = new Array(), e = 0; e < this.asn1Array.length; e++) {
      var i = this.asn1Array[e]
      t.push(i.getEncodedHex())
    }
    return t.sort(), (this.hV = t.join('')), this.hV
  }
}
Ce.extend(KJUR.asn1.DERSet, KJUR.asn1.DERAbstractStructured)
KJUR.asn1.DERTaggedObject = function (t) {
  KJUR.asn1.DERTaggedObject.superclass.constructor.call(this)
  this.hT = 'a0'
  this.hV = ''
  this.isExplicit = true
  this.asn1Object = null
  this.setASN1Object = function (t, e, i) {
    this.hT = e
    this.isExplicit = t
    this.asn1Object = i
    this.isExplicit
      ? ((this.hV = this.asn1Object.getEncodedHex()),
        (this.hTLV = null),
        (this.isModified = true))
      : ((this.hV = null),
        (this.hTLV = i.getEncodedHex()),
        (this.hTLV = this.hTLV.replace(/^../, e)),
        (this.isModified = false))
  }
  this.getFreshValueHex = function () {
    return this.hV
  }
  'undefined' != typeof t &&
    ('undefined' != typeof t.tag && (this.hT = t.tag),
    'undefined' != typeof t.explicit && (this.isExplicit = t.explicit),
    'undefined' != typeof t.obj &&
      ((this.asn1Object = t.obj),
      this.setASN1Object(this.isExplicit, this.hT, this.asn1Object)))
}
Ce.extend(KJUR.asn1.DERTaggedObject, KJUR.asn1.ASN1Object)
;(function (t) {
  'use strict'
  var e,
    i = {
      decode: function (i) {
        var r
        if (e === t) {
          var s = '0123456789ABCDEF'
          for (e = [], r = 0; 16 > r; ++r) {
            e[s.charAt(r)] = r
          }
          for (s = s.toLowerCase(), r = 10; 16 > r; ++r) {
            e[s.charAt(r)] = r
          }
          for (r = 0; r < ' \\f\\n\\r  Â \\u2028\\u2029'.length; ++r) {
            e[' \\f\\n\\r  Â \\u2028\\u2029'.charAt(r)] = -1
          }
        }
        var o = [],
          h = 0,
          a = 0
        for (r = 0; r < i.length; ++r) {
          var u = i.charAt(r)
          if ('=' == u) {
            break
          }
          if (((u = e[u]), -1 != u)) {
            if (u === t) {
              throw 'Illegal character at offset ' + r
            }
            h |= u
            ++a >= 2 ? ((o[o.length] = h), (h = 0), (a = 0)) : (h <<= 4)
          }
        }
        if (a) {
          throw 'Hex encoding incomplete: 4 bits missing'
        }
        return o
      },
    }
  NewWindow.Hex = i
})()
;(function (t) {
  'use strict'
  var e,
    i = {
      decode: function (i) {
        var r
        if (e === t) {
          for (e = [], r = 0; 64 > r; ++r) {
            e[
              'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.charAt(
                r
              )
            ] = r
          }
          for (r = 0; r < '= \\f\\n\\r Â \\u2028\\u2029'.length; ++r) {
            e['= \\f\\n\\r Â \\u2028\\u2029'.charAt(r)] = -1
          }
        }
        var o = [],
          h = 0,
          a = 0
        for (r = 0; r < i.length; ++r) {
          var u = i.charAt(r)
          if ('=' == u) {
            break
          }
          if (((u = e[u]), -1 != u)) {
            if (u === t) {
              throw 'Illegal character at offset ' + r
            }
            h |= u
            ++a >= 4
              ? ((o[o.length] = h >> 16),
                (o[o.length] = (h >> 8) & 255),
                (o[o.length] = 255 & h),
                (h = 0),
                (a = 0))
              : (h <<= 6)
          }
        }
        switch (a) {
          case 1:
            throw 'Base64 encoding incomplete: at least 2 bits missing'
          case 2:
            o[o.length] = h >> 10
            break
          case 3:
            ;(o[o.length] = h >> 16), (o[o.length] = (h >> 8) & 255)
        }
        return o
      },
      re: /-----BEGIN [^-]+-----([A-Za-z0-9+\\/=\\s]+)-----END [^-]+-----|begin-base64[^\\n]+\\n([A-Za-z0-9+\\/=\\s]+)====/,
      unarmor: function (t) {
        var e = i.re.exec(t)
        if (e) {
          if (e[1]) {
            t = e[1]
          } else {
            if (!e[2]) {
              throw 'RegExp out of sync'
            }
            t = e[2]
          }
        }
        return i.decode(t)
      },
    }
  NewWindow.Base64 = i
})()
;(function (t) {
  'use strict'
  function e(t, i) {
    t instanceof e
      ? ((this.enc = t.enc), (this.pos = t.pos))
      : ((this.enc = t), (this.pos = i))
  }
  function i(t, e, i, r, s) {
    this.stream = t
    this.header = e
    this.length = i
    this.tag = r
    this.sub = s
  }
  var n = {
    tag: function (t, e) {
      var i = document.createElement(t)
      return (i.className = e), i
    },
    text: function (t) {
      return document.createTextNode(t)
    },
  }
  e.prototype.get = function (e) {
    if ((e === t && (e = this.pos++), e >= this.enc.length)) {
      throw (
        'Requesting byte offset ' +
        e +
        ' on a stream of length ' +
        this.enc.length
      )
    }
    return this.enc[e]
  }
  e.prototype.hexDigits = '0123456789ABCDEF'
  e.prototype.hexByte = function (t) {
    return this.hexDigits.charAt((t >> 4) & 15) + this.hexDigits.charAt(15 & t)
  }
  e.prototype.hexDump = function (t, e, i) {
    for (var r = '', s = t; e > s; ++s) {
      if (((r += this.hexByte(this.get(s))), i !== true)) {
        switch (15 & s) {
          case 7:
            r += '  '
            break
          case 15:
            r += '\\n'
            break
          default:
            r += ' '
        }
      }
    }
    return r
  }
  e.prototype.parseStringISO = function (t, e) {
    for (var i = '', r = t; e > r; ++r) {
      i += String.fromCharCode(this.get(r))
    }
    return i
  }
  e.prototype.parseStringUTF = function (t, e) {
    for (var i = '', r = t; e > r; ) {
      var s = this.get(r++)
      i +=
        128 > s
          ? String.fromCharCode(s)
          : s > 191 && 224 > s
          ? String.fromCharCode(((31 & s) << 6) | (63 & this.get(r++)))
          : String.fromCharCode(
              ((15 & s) << 12) |
                ((63 & this.get(r++)) << 6) |
                (63 & this.get(r++))
            )
    }
    return i
  }
  e.prototype.parseStringBMP = function (t, e) {
    for (var i = '', r = t; e > r; r += 2) {
      var s = this.get(r),
        n = this.get(r + 1)
      i += String.fromCharCode((s << 8) + n)
    }
    return i
  }
  e.prototype.reTime =
    /^((?:1[89]|2\\d)?\\d\\d)(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])([01]\\d|2[0-3])(?:([0-5]\\d)(?:([0-5]\\d)(?:[.,](\\d{1,3}))?)?)?(Z|[-+](?:[0]\\d|1[0-2])([0-5]\\d)?)?$/
  e.prototype.parseTime = function (t, e) {
    var i = this.parseStringISO(t, e),
      r = this.reTime.exec(i)
    return r
      ? ((i = r[1] + '-' + r[2] + '-' + r[3] + ' ' + r[4]),
        r[5] &&
          ((i += ':' + r[5]),
          r[6] && ((i += ':' + r[6]), r[7] && (i += '.' + r[7]))),
        r[8] &&
          ((i += ' UTC'),
          'Z' != r[8] && ((i += r[8]), r[9] && (i += ':' + r[9]))),
        i)
      : 'Unrecognized time: ' + i
  }
  e.prototype.parseInteger = function (t, e) {
    var i = e - t
    if (i > 4) {
      i <<= 3
      var r = this.get(t)
      if (0 === r) {
        i -= 8
      } else {
        for (; 128 > r; ) {
          r <<= 1
          --i
        }
      }
      return '(' + i + ' bit)'
    }
    for (var s = 0, n = t; e > n; ++n) {
      s = (s << 8) | this.get(n)
    }
    return s
  }
  e.prototype.parseBitString = function (t, e) {
    var i = this.get(t),
      r = ((e - t - 1) << 3) - i,
      s = '(' + r + ' bit)'
    if (20 >= r) {
      var n = i
      s += ' '
      for (var o = e - 1; o > t; --o) {
        for (var h = this.get(o), a = n; 8 > a; ++a) {
          s += (h >> a) & 1 ? '1' : '0'
        }
        n = 0
      }
    }
    return s
  }
  e.prototype.parseOctetString = function (t, e) {
    var i = e - t,
      n = '(' + i + ' byte) '
    i > 100 && (e = t + 100)
    for (var o = t; e > o; ++o) {
      n += this.hexByte(this.get(o))
    }
    return i > 100 && (n += 'â\\u20AC\\xA6'), n
  }
  e.prototype.parseOID = function (t, e) {
    for (var i = '', r = 0, s = 0, n = t; e > n; ++n) {
      var o = this.get(n)
      if (((r = (r << 7) | (127 & o)), (s += 7), !(128 & o))) {
        if ('' === i) {
          var h = 80 > r ? (40 > r ? 0 : 1) : 2
          i = h + '.' + (r - 40 * h)
        } else {
          i += '.' + (s >= 31 ? 'bigint' : r)
        }
        r = s = 0
      }
    }
    return i
  }
  i.prototype.typeName = function () {
    if (this.tag === t) {
      return 'unknown'
    }
    var e = this.tag >> 6,
      i = ((this.tag >> 5) & 1, 31 & this.tag)
    switch (e) {
      case 0:
        switch (i) {
          case 0:
            return 'EOC'
          case 1:
            return 'BOOLEAN'
          case 2:
            return 'INTEGER'
          case 3:
            return 'BIT_STRING'
          case 4:
            return 'OCTET_STRING'
          case 5:
            return 'NULL'
          case 6:
            return 'OBJECT_IDENTIFIER'
          case 7:
            return 'ObjectDescriptor'
          case 8:
            return 'EXTERNAL'
          case 9:
            return 'REAL'
          case 10:
            return 'ENUMERATED'
          case 11:
            return 'EMBEDDED_PDV'
          case 12:
            return 'UTF8String'
          case 16:
            return 'SEQUENCE'
          case 17:
            return 'SET'
          case 18:
            return 'NumericString'
          case 19:
            return 'PrintableString'
          case 20:
            return 'TeletexString'
          case 21:
            return 'VideotexString'
          case 22:
            return 'IA5String'
          case 23:
            return 'UTCTime'
          case 24:
            return 'GeneralizedTime'
          case 25:
            return 'GraphicString'
          case 26:
            return 'VisibleString'
          case 27:
            return 'GeneralString'
          case 28:
            return 'UniversalString'
          case 30:
            return 'BMPString'
          default:
            return 'Universal_' + i.toString(16)
        }
      case 1:
        return 'Application_' + i.toString(16)
      case 2:
        return '[' + i + ']'
      case 3:
        return 'Private_' + i.toString(16)
    }
  }
  i.prototype.reSeemsASCII = /^[ -~]+$/
  i.prototype.content = function () {
    if (this.tag === t) {
      return null
    }
    var e = this.tag >> 6,
      i = 31 & this.tag,
      n = this.posContent(),
      o = Math.abs(this.length)
    if (0 !== e) {
      if (null !== this.sub) {
        return '(' + this.sub.length + ' elem)'
      }
      var h = this.stream.parseStringISO(n, n + Math.min(o, 100))
      return this.reSeemsASCII.test(h)
        ? h.substring(0, 200) + (h.length > 200 ? 'â\\u20AC\\xA6' : '')
        : this.stream.parseOctetString(n, n + o)
    }
    switch (i) {
      case 1:
        return 0 === this.stream.get(n) ? 'false' : 'true'
      case 2:
        return this.stream.parseInteger(n, n + o)
      case 3:
        return this.sub
          ? '(' + this.sub.length + ' elem)'
          : this.stream.parseBitString(n, n + o)
      case 4:
        return this.sub
          ? '(' + this.sub.length + ' elem)'
          : this.stream.parseOctetString(n, n + o)
      case 6:
        return this.stream.parseOID(n, n + o)
      case 16:
      case 17:
        return '(' + this.sub.length + ' elem)'
      case 12:
        return this.stream.parseStringUTF(n, n + o)
      case 18:
      case 19:
      case 20:
      case 21:
      case 22:
      case 26:
        return this.stream.parseStringISO(n, n + o)
      case 30:
        return this.stream.parseStringBMP(n, n + o)
      case 23:
      case 24:
        return this.stream.parseTime(n, n + o)
    }
    return null
  }
  i.prototype.toString = function () {
    return (
      this.typeName() +
      '@' +
      this.stream.pos +
      '[header:' +
      this.header +
      ',length:' +
      this.length +
      ',sub:' +
      (null === this.sub ? 'null' : this.sub.length) +
      ']'
    )
  }
  i.prototype.print = function (e) {
    if ((e === t && (e = ''), document.writeln(e + this), null !== this.sub)) {
      e += '  '
      for (var i = 0, r = this.sub.length; r > i; ++i) {
        this.sub[i].print(e)
      }
    }
  }
  i.prototype.toPrettyString = function (e) {
    e === t && (e = '')
    var i = e + this.typeName() + ' @' + this.stream.pos
    if (
      (this.length >= 0 && (i += '+'),
      (i += this.length),
      32 & this.tag
        ? (i += ' (constructed)')
        : (3 != this.tag && 4 != this.tag) ||
          null === this.sub ||
          (i += ' (encapsulates)'),
      (i += '\\n'),
      null !== this.sub)
    ) {
      e += '  '
      for (var r = 0, s = this.sub.length; s > r; ++r) {
        i += this.sub[r].toPrettyString(e)
      }
    }
    return i
  }
  i.prototype.toDOM = function () {
    var t = n.tag('div', 'node')
    t.asn1 = this
    var e = n.tag('div', 'head'),
      i = this.typeName().replace(/_/g, ' ')
    e.innerHTML = i
    var r = this.content()
    if (null !== r) {
      r = String(r).replace(/</g, '&lt;')
      var s = n.tag('span', 'preview')
      s.appendChild(n.text(r))
      e.appendChild(s)
    }
    t.appendChild(e)
    this.node = t
    this.head = e
    var o = n.tag('div', 'value')
    if (
      ((i = 'Offset: ' + this.stream.pos + '<br/>'),
      (i += 'Length: ' + this.header + '+'),
      (i += this.length >= 0 ? this.length : -this.length + ' (undefined)'),
      32 & this.tag
        ? (i += '<br/>(constructed)')
        : (3 != this.tag && 4 != this.tag) ||
          null === this.sub ||
          (i += '<br/>(encapsulates)'),
      null !== r &&
        ((i += '<br/>Value:<br/><b>' + r + '</b>'),
        'object' == typeof oids && 6 == this.tag))
    ) {
      var h = oids[r]
      h &&
        (h.d && (i += '<br/>' + h.d),
        h.c && (i += '<br/>' + h.c),
        h.w && (i += '<br/>(warning!)'))
    }
    o.innerHTML = i
    t.appendChild(o)
    var a = n.tag('div', 'sub')
    if (null !== this.sub) {
      for (var u = 0, c = this.sub.length; c > u; ++u) {
        a.appendChild(this.sub[u].toDOM())
      }
    }
    return (
      t.appendChild(a),
      (e.onclick = function () {
        t.className =
          'node collapsed' == t.className ? 'node' : 'node collapsed'
      }),
      t
    )
  }
  i.prototype.posStart = function () {
    return this.stream.pos
  }
  i.prototype.posContent = function () {
    return this.stream.pos + this.header
  }
  i.prototype.posEnd = function () {
    return this.stream.pos + this.header + Math.abs(this.length)
  }
  i.prototype.fakeHover = function (t) {
    this.node.className += ' hover'
    t && (this.head.className += ' hover')
  }
  i.prototype.fakeOut = function (t) {
    this.node.className = this.node.className.replace(/ ?hover/, '')
    t && (this.head.className = this.head.className.replace(/ ?hover/, ''))
  }
  i.prototype.toHexDOM_sub = function (t, e, i, r, s) {
    if (!(r >= s)) {
      var o = n.tag('span', e)
      o.appendChild(n.text(i.hexDump(r, s)))
      t.appendChild(o)
    }
  }
  i.prototype.toHexDOM = function (e) {
    var i = n.tag('span', 'hex')
    if (
      (e === t && (e = i),
      (this.head.hexNode = i),
      (this.head.onmouseover = function () {
        this.hexNode.className = 'hexCurrent'
      }),
      (this.head.onmouseout = function () {
        this.hexNode.className = 'hex'
      }),
      (i.asn1 = this),
      (i.onmouseover = function () {
        var t = !e.selected
        t && ((e.selected = this.asn1), (this.className = 'hexCurrent'))
        this.asn1.fakeHover(t)
      }),
      (i.onmouseout = function () {
        var t = e.selected == this.asn1
        this.asn1.fakeOut(t)
        t && ((e.selected = null), (this.className = 'hex'))
      }),
      this.toHexDOM_sub(
        i,
        'tag',
        this.stream,
        this.posStart(),
        this.posStart() + 1
      ),
      this.toHexDOM_sub(
        i,
        this.length >= 0 ? 'dlen' : 'ulen',
        this.stream,
        this.posStart() + 1,
        this.posContent()
      ),
      null === this.sub)
    ) {
      i.appendChild(
        n.text(this.stream.hexDump(this.posContent(), this.posEnd()))
      )
    } else {
      if (this.sub.length > 0) {
        var r = this.sub[0],
          s = this.sub[this.sub.length - 1]
        this.toHexDOM_sub(
          i,
          'intro',
          this.stream,
          this.posContent(),
          r.posStart()
        )
        for (var o = 0, h = this.sub.length; h > o; ++o) {
          i.appendChild(this.sub[o].toHexDOM(e))
        }
        this.toHexDOM_sub(i, 'outro', this.stream, s.posEnd(), this.posEnd())
      }
    }
    return i
  }
  i.prototype.toHexString = function (t) {
    return this.stream.hexDump(this.posStart(), this.posEnd(), true)
  }
  i.decodeLength = function (t) {
    var e = t.get(),
      i = 127 & e
    if (i == e) {
      return i
    }
    if (i > 3) {
      throw 'Length over 24 bits not supported at position ' + (t.pos - 1)
    }
    if (0 === i) {
      return -1
    }
    e = 0
    for (var r = 0; i > r; ++r) {
      e = (e << 8) | t.get()
    }
    return e
  }
  i.hasContent = function (t, r, s) {
    if (32 & t) {
      return true
    }
    if (3 > t || t > 4) {
      return false
    }
    var n = new e(s)
    3 == t && n.get()
    var o = n.get()
    if ((o >> 6) & 1) {
      return false
    }
    try {
      var h = i.decodeLength(n)
      return n.pos - s.pos + h == r
    } catch (a) {
      return false
    }
  }
  i.decode = function (t) {
    t instanceof e || (t = new e(t, 0))
    var r = new e(t),
      s = t.get(),
      n = i.decodeLength(t),
      o = t.pos - r.pos,
      h = null
    if (i.hasContent(s, n, t)) {
      var a = t.pos
      if ((3 == s && t.get(), (h = []), n >= 0)) {
        for (var u = a + n; t.pos < u; ) {
          h[h.length] = i.decode(t)
        }
        if (t.pos != u) {
          throw (
            'Content size is not correct for container starting at offset ' + a
          )
        }
      } else {
        try {
          for (;;) {
            var c = i.decode(t)
            if (0 === c.tag) {
              break
            }
            h[h.length] = c
          }
          n = a - t.pos
        } catch (f) {
          throw 'Exception while decoding undefined length content: ' + f
        }
      }
    } else {
      t.pos += n
    }
    return new i(r, o, n, s, h)
  }
  i.test = function () {
    for (
      var t = [
          {
            value: [39],
            expected: 39,
          },
          {
            value: [129, 201],
            expected: 201,
          },
          {
            value: [131, 254, 220, 186],
            expected: 16702650,
          },
        ],
        r = 0,
        s = t.length;
      s > r;
      ++r
    ) {
      var n = new e(t[r].value, 0),
        o = i.decodeLength(n)
      o != t[r].expected &&
        document.write(
          'In test[' + r + '] expected ' + t[r].expected + ' got ' + o + '\\n'
        )
    }
  }
  NewWindow.ASN1 = i
})()
NewWindow.ASN1.prototype.getHexStringValue = function () {
  var t = this.toHexString(),
    e = 2 * this.header,
    i = 2 * this.length
  return t.substr(e, i)
}
ue.prototype.parseKey = function (t) {
  try {
    var e = 0,
      i = 0,
      s = /^\\s*(?:[0-9A-Fa-f][0-9A-Fa-f]\\s*)+$/.test(t)
        ? NewWindow.Hex.decode(t)
        : NewWindow.Base64.unarmor(t),
      n = NewWindow.ASN1.decode(s)
    if ((3 === n.sub.length && (n = n.sub[2].sub[0]), 9 === n.sub.length)) {
      e = n.sub[1].getHexStringValue()
      this.n = he(e, 16)
      i = n.sub[2].getHexStringValue()
      this.e = parseInt(i, 16)
      var o = n.sub[3].getHexStringValue()
      this.d = he(o, 16)
      var h = n.sub[4].getHexStringValue()
      this.p = he(h, 16)
      var a = n.sub[5].getHexStringValue()
      this.q = he(a, 16)
      var u = n.sub[6].getHexStringValue()
      this.dmp1 = he(u, 16)
      var c = n.sub[7].getHexStringValue()
      this.dmq1 = he(c, 16)
      var f = n.sub[8].getHexStringValue()
      this.coeff = he(f, 16)
    } else {
      if (2 !== n.sub.length) {
        return false
      }
      var p = n.sub[1],
        l = p.sub[0]
      e = l.sub[0].getHexStringValue()
      this.n = he(e, 16)
      i = l.sub[1].getHexStringValue()
      this.e = parseInt(i, 16)
    }
    return true
  } catch (d) {
    return false
  }
}
ue.prototype.getPrivateBaseKey = function () {
  var t = {
      array: [
        new KJUR.asn1.DERInteger({ int: 0 }),
        new KJUR.asn1.DERInteger({ bigint: this.n }),
        new KJUR.asn1.DERInteger({ int: this.e }),
        new KJUR.asn1.DERInteger({ bigint: this.d }),
        new KJUR.asn1.DERInteger({ bigint: this.p }),
        new KJUR.asn1.DERInteger({ bigint: this.q }),
        new KJUR.asn1.DERInteger({ bigint: this.dmp1 }),
        new KJUR.asn1.DERInteger({ bigint: this.dmq1 }),
        new KJUR.asn1.DERInteger({ bigint: this.coeff }),
      ],
    },
    e = new KJUR.asn1.DERSequence(t)
  return e.getEncodedHex()
}
ue.prototype.getPrivateBaseKeyB64 = function () {
  return be(this.getPrivateBaseKey())
}
ue.prototype.getPublicBaseKey = function () {
  var t = {
      array: [
        new KJUR.asn1.DERObjectIdentifier({ oid: '1.2.840.113549.1.1.1' }),
        new KJUR.asn1.DERNull(),
      ],
    },
    e = new KJUR.asn1.DERSequence(t)
  t = {
    array: [
      new KJUR.asn1.DERInteger({ bigint: this.n }),
      new KJUR.asn1.DERInteger({ int: this.e }),
    ],
  }
  var i = new KJUR.asn1.DERSequence(t)
  t = { hex: '00' + i.getEncodedHex() }
  var r = new KJUR.asn1.DERBitString(t)
  t = {
    array: [e, r],
  }
  var s = new KJUR.asn1.DERSequence(t)
  return s.getEncodedHex()
}
ue.prototype.getPublicBaseKeyB64 = function () {
  return be(this.getPublicBaseKey())
}
ue.prototype.wordwrap = function (t, e) {
  if (((e = e || 64), !t)) {
    return t
  }
  var i = '(.{1,' + e + '})( +|$\\n?)|(.{1,' + e + '})'
  return t.match(RegExp(i, 'g')).join('\\n')
}
ue.prototype.getPrivateKey = function () {
  var t = '-----BEGIN RSA PRIVATE KEY-----\\n'
  return (
    (t += this.wordwrap(this.getPrivateBaseKeyB64()) + '\\n'),
    (t += '-----END RSA PRIVATE KEY-----')
  )
}
ue.prototype.getPublicKey = function () {
  var t = '-----BEGIN PUBLIC KEY-----\\n'
  return (
    (t += this.wordwrap(this.getPublicBaseKeyB64()) + '\\n'),
    (t += '-----END PUBLIC KEY-----')
  )
}
ue.prototype.hasPublicKeyProperty = function (t) {
  return (t = t || {}), t.hasOwnProperty('n') && t.hasOwnProperty('e')
}
ue.prototype.hasPrivateKeyProperty = function (t) {
  return (
    (t = t || {}),
    t.hasOwnProperty('n') &&
      t.hasOwnProperty('e') &&
      t.hasOwnProperty('d') &&
      t.hasOwnProperty('p') &&
      t.hasOwnProperty('q') &&
      t.hasOwnProperty('dmp1') &&
      t.hasOwnProperty('dmq1') &&
      t.hasOwnProperty('coeff')
  )
}
ue.prototype.parsePropertiesFrom = function (t) {
  this.n = t.n
  this.e = t.e
  t.hasOwnProperty('d') &&
    ((this.d = t.d),
    (this.p = t.p),
    (this.q = t.q),
    (this.dmp1 = t.dmp1),
    (this.dmq1 = t.dmq1),
    (this.coeff = t.coeff))
}
var _e = function (t) {
  ue.call(this)
  t &&
    ('string' == typeof t
      ? this.parseKey(t)
      : (this.hasPrivateKeyProperty(t) || this.hasPublicKeyProperty(t)) &&
        this.parsePropertiesFrom(t))
}
_e.prototype = new ue()
_e.prototype.constructor = _e
var ze = function (t) {
  t = t || {}
  this.default_key_size = parseInt(t.default_key_size) || 1024
  this.default_public_exponent = t.default_public_exponent || '010001'
  this.log = t.log || false
  this.key = null
}
ze.prototype.setKey = function (t) {
  this.log &&
    this.key &&
    console.warn('A key was already set, overriding existing.')
  this.key = new _e(t)
}
ze.prototype.setPrivateKey = function (t) {
  this.setKey(t)
}
ze.prototype.setPublicKey = function (t) {
  this.setKey(t)
}
ze.prototype.decrypt = function (t) {
  try {
    return this.getKey().decrypt(Te(t))
  } catch (e) {
    return false
  }
}
ze.prototype.encrypt = function (t) {
  try {
    return be(this.getKey().encrypt(t))
  } catch (e) {
    return false
  }
}
ze.prototype.getKey = function (t) {
  if (!this.key) {
    if (
      ((this.key = new _e()), t && '[object Function]' === {}.toString.call(t))
    ) {
      return void this.key.generateAsync(
        this.default_key_size,
        this.default_public_exponent,
        t
      )
    }
    this.key.generate(this.default_key_size, this.default_public_exponent)
  }
  return this.key
}
ze.prototype.getPrivateKey = function () {
  return this.getKey().getPrivateKey()
}
ze.prototype.getPrivateKeyB64 = function () {
  return this.getKey().getPrivateBaseKeyB64()
}
ze.prototype.getPublicKey = function () {
  return this.getKey().getPublicKey()
}
ze.prototype.getPublicKeyB64 = function () {
  return this.getKey().getPublicBaseKeyB64()
}
ze.version = '2.3.1'
const JSEncrypt = ze

function encrypt(eobC1) {
  var aRSzQ$2 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJFmw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9ZmmaFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4ebooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyjfey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8LgbbWQIDAQAB";
  var GDtZO3 = new JSEncrypt;
  GDtZO3.setPublicKey(aRSzQ$2);
  var qdfHwVm4 = GDtZO3.encrypt(eobC1);
  return qdfHwVm4;
}
"""


class QueryApi:
  LoginIndex                  = 'https://login.gjzwfw.gov.cn'
  NaturalFwd                  = 'https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/naturalFwd'
  CsrfSave                    = 'https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/csrfSave'
  UploadIdentifier            = 'https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/uploadIdentifier'
  VerifyCodeImg               = 'https://login.gjzwfw.gov.cn/tacs-uc/verify/verifyCodeImg?rnd='
  ForgetPwdFirst              = 'https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/forgetPwdFirst?times='
  ForgetImmigrationPwdFirst   = 'https://login.gjzwfw.gov.cn/tacs-uc/naturalMan/forgetImmigrationPwdFirst?times='
  BaseHeaders                 = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"macOS\"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  }
  IdInquirerQuestion          = [
    inquirer.List(
      'idType',
      message='證件類別',
      choices=['中华人民共和国居民身份证', '港澳居民来往内地通行证', '台湾居民来往大陆通行证', '中华人民共和国普通护照 (国家移民管理局签发)', '外国人永久居留身份证', '台湾居民居住证', '港澳居民居住证'],
    ),
  ];

  @staticmethod
  def merge_headers(headers: dict[str, str]) -> dict[str, str]:
    base_headers = copy.deepcopy(QueryApi.BaseHeaders)
    return headers | base_headers

  @staticmethod
  def index_fetch(session, connect_timeout : int, read_timeout : int) -> requests.models.Response:
    return session.get(QueryApi.NaturalFwd, stream = True, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Referer': (QueryApi.LoginIndex + '/'),
      })
    );

  @staticmethod
  def csrf_fetch(session, cookies : requests.cookies.RequestsCookieJar, connect_timeout : int, read_timeout : int) -> requests.models.Response:
    return session.post(QueryApi.CsrfSave, stream = True, cookies = cookies, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': QueryApi.LoginIndex,
        'Referer': QueryApi.NaturalFwd,
      })
    );

  @staticmethod
  def generated_uuid_fetch(pymonkey, session, cookies : requests.cookies.RequestsCookieJar, csrf_token : str, connect_timeout : int, read_timeout : int) -> requests.models.Response:
    return session.post(QueryApi.UploadIdentifier, stream = True, cookies = cookies, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': QueryApi.LoginIndex,
        'Referer': QueryApi.NaturalFwd,
        'Token': pm.globalThis.encrypt(csrf_token),
      })
    );

  @staticmethod
  def captcha_fetch(session, cookies : requests.cookies.RequestsCookieJar, connect_timeout : int, read_timeout : int) -> requests.models.Response:
    return session.get((QueryApi.VerifyCodeImg + str(random.random())), stream = True, cookies = cookies, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Referer': QueryApi.NaturalFwd,
      })
    );

  @staticmethod
  def final_challenge_fetch(pymonkey, session, cookies : requests.cookies.RequestsCookieJar, connect_timeout : int, read_timeout : int, generated_uuid : str, csrf_token : str, user_name : str,  cert_no : str, cert_type : str, captcha_text : str) -> requests.models.Response:
    # Default.
    forget_first = QueryApi.ForgetPwdFirst + generated_uuid;

    # Regular Id Card
    if cert_no != '111':
      forget_first = QueryApi.ForgetImmigrationPwdFirst + generated_uuid;

    # Session Handle.
    return session.post((QueryApi.ForgetPwdFirst + generated_uuid), stream = True, cookies = cookies, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': QueryApi.NaturalFwd,
        'Token': pm.globalThis.encrypt(csrf_token),
      }), data = {
        'userName': user_name,
        'certNo': pm.globalThis.encrypt(cert_no),
        'certType': cert_type,
        'staticCode': captcha_text
      }
    );

  @staticmethod
  def final_fetch(session, cookies : requests.cookies.RequestsCookieJar, connect_timeout : int, read_timeout : int) -> requests.models.Response:
    return session.get(QueryApi.NaturalFwd, stream = True, cookies = cookies, timeout = (connect_timeout, read_timeout), headers = QueryApi.merge_headers(headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Referer': QueryApi.NaturalFwd,
      })
    );

  @staticmethod
  def query(pymonkey, ocr : ddddocr.DdddOcr, max_retries : int, user_name : str, cert_no : str, cert_type : str) -> dict:
    loop_times = 0;
    errors = [];

    while True:
      if loop_times >= max_retries:
        return { 'errorCode': 15010, 'exception': None, 'reason': 'loop_times > max_retries!', 'errors': errors }

      # Call.
      result = QueryApi.__query(pymonkey = pymonkey, ocr = ocr, user_name = user_name, cert_no = cert_no, cert_type = cert_type);

      # Passport or Other Id Card.
      if (result['errorCode'] == 13410) and (cert_type != '111'):
        return result;

      # Retries
      if result['errorCode'] != 0:
        loop_times += 1;
        errors.append(result);

        continue
      else:
        # Final.
        result['errors'] = errors;
        return result;



  @staticmethod
  def __query(pymonkey, ocr : ddddocr.DdddOcr, user_name : str, cert_no : str, cert_type : str) -> dict:
    session = requests.Session();

    try:
        # Init SessionId.
        index_response = QueryApi.index_fetch(session = session, connect_timeout = 5, read_timeout = 5);
    except Exception as ex:
        return { 'errorCode': 12100, 'exception': ex, 'reason': None }

    try:
        # Generate CsrfToken.
        csrf_response = QueryApi.csrf_fetch(session = session, cookies = index_response.cookies, connect_timeout = 5, read_timeout = 5);

        # Parse JSON.
        response_text = csrf_response.raw.read(4096, decode_content = True).decode('utf-8');
        parsed_json = json.loads(response_text);
        csrf_token = parsed_json['data'];
    except Exception as ex:
        return { 'errorCode': 12101, 'exception': ex, 'reason': None }

    try:
        # Generate UUID.
        generated_uuid_response = QueryApi.generated_uuid_fetch(pymonkey = pymonkey, session = session, cookies = csrf_response.cookies, connect_timeout = 5, read_timeout = 5, csrf_token = csrf_token);


        # Parse JSON.
        response_text = generated_uuid_response.raw.read(4096, decode_content = True).decode('utf-8');
        parsed_json = json.loads(response_text);
        generated_uuid = parsed_json['data'];
    except Exception as ex:
        return { 'errorCode': 12102, 'exception': ex, 'reason': None }

    try:
        # Get Captcha.
        captcha_response = QueryApi.captcha_fetch(session = session, cookies = generated_uuid_response.cookies, connect_timeout = 5, read_timeout = 5);

        # Socket Read.
        response_bytes = captcha_response.raw.read(65536, decode_content = False);
    except Exception as ex:
        return { 'errorCode': 12103, 'exception': ex, 'reason': None }

    try:
        # Get CsrfToken.
        csrf_response = QueryApi.csrf_fetch(session = session, cookies = captcha_response.cookies, connect_timeout = 5, read_timeout = 5);

        # Parse JSON.
        response_text = csrf_response.raw.read(4096, decode_content = True).decode('utf-8');
        parsed_json = json.loads(response_text);
        csrf_token = parsed_json['data'];
    except Exception as ex:
        return { 'errorCode': 12104, 'exception': ex, 'reason': None }

    try:
        # Captcha OCR.
        captcha_text = ocr.classification(response_bytes);
    except Exception as ex:
        return { 'errorCode': 12105, 'exception': ex, 'reason': None }

    try:
        # Final Challenge.
        final_challenge_response = QueryApi.final_challenge_fetch(pymonkey = pymonkey, session = session, cookies = csrf_response.cookies, connect_timeout = 5, read_timeout = 5, 
          generated_uuid = generated_uuid, csrf_token = csrf_token, 
          user_name = user_name, cert_no = cert_no, cert_type = cert_type, captcha_text = captcha_text);

        # Parse JSON.
        response_text = final_challenge_response.raw.read(65536, decode_content = True).decode('utf-8');
        final_challenge_json = json.loads(response_text);

        # Passport or Other Type (The ID information is wrong or not registered, please check the input information.)
        if final_challenge_json['code'] == '90131':
          return { 'errorCode': 13410, 'exception': None, 'reason': final_challenge_json['msg'] }

        # Challenge failed.
        if final_challenge_json['code'] != '90000':
          return { 'errorCode': 13101, 'exception': None, 'reason': final_challenge_json['msg'] }
    except Exception as ex:
        return { 'errorCode': 12106, 'exception': ex, 'reason': None }

    try:
        # Final.
        final_response = QueryApi.final_fetch(session = session, cookies = final_challenge_response.cookies, connect_timeout = 5, read_timeout = 5);

        # Socket Read.
        response_text = final_response.raw.read(65536, decode_content = True).decode('utf-8');
        scan_result = re.findall(r'<span class=\"colblur\">(.*?)</span>', response_text); 

        # Find masked or handle Unknown.
        if len(scan_result) == 2:
          return { 'errorCode': 0, 'exception': None, 'maskedCertNo': scan_result[0], 'maskedPhoneNumber': scan_result[1] }
        else:
          return { 'errorCode': 13100, 'exception': None, 'reason': 'Unknown reason, regular expression matching failed!' }
    except Exception as ex:
        return { 'errorCode': 12107, 'exception': ex, 'reason': None }

  @staticmethod
  def ask_id_type() -> str:
    questions = QueryApi.IdInquirerQuestion;
    selected_type = inquirer.prompt(questions);

    # Equal KeyboardInterrupt.
    if selected_type == None:
      print('終止選取!');
      exit();

    answers = selected_type['idType'];

    if answers == '中华人民共和国居民身份证':
      return '111';
    elif answers == '港澳居民来往内地通行证':
      return '516';
    elif answers == '台湾居民来往大陆通行证':
      return '511';
    elif answers == '中华人民共和国普通护照 (国家移民管理局签发)':
      return '414';
    elif answers == '外国人永久居留身份证':
      return '553';
    elif answers == '台湾居民居住证':
      return '155';
    elif answers == '港澳居民居住证':
      return '156';
    else:
      # Default Regular IdCard.
      return '111';


  @staticmethod
  def cli_interface(pymonkey, ocr : ddddocr.DdddOcr):
    while True:
      # Ask Id Type.
      choice_id_type = QueryApi.ask_id_type();

      # Check Regular IdCard.
      if choice_id_type == '111':
        # Ask UserName.
        while True:
          try:
              user_name = input('輸入姓名: ');
          except KeyboardInterrupt:
              print('終止輸入!');
              exit();

          if len(user_name) > 4 or len(user_name) < 2:
            print('您輸入的姓名有誤!');
            continue;

          if re.match('^[0-9a-zA-Z]*$', user_name):
            print('\r\n您輸入的姓名有誤!');
            continue;
          else:
            break;

          if not re.match(r'[\u4e00-\u9fff]+', user_name):
            print('您輸入的姓名有誤!');
            continue;
          else:
            break;

        # Ask CertNo.
        while True:
          try:
              cert_no = input('輸入身分證: ');
          except KeyboardInterrupt:
              print('\r\n終止輸入!');
              exit();

          if not re.match('^[0-9xX]*$', cert_no):
            print('您輸入的身分證有誤!');
            continue;
          else:
            break;

          if re.match(r'[\u4e00-\u9fff]+', user_name):
            print('您輸入的身分證有誤!');
            continue;
          else:
            break;

          if len(cert_no) != 18:
            print('您輸入的身分證有誤!');
            continue;
          else:
            break;

      else:
        # Ask UserName.
        while True:
          try:
              user_name = input('輸入姓名: ');
          except KeyboardInterrupt:
              print('終止輸入!');
              exit();

          if re.match('^[0-9]*$', user_name):
            print('\r\n您輸入的姓名有誤!');
            continue;
          else:
            break;

        # Ask CertNo.
        while True:
          try:
              cert_no = input('輸入證件號: ');
          except KeyboardInterrupt:
              print('\r\n終止輸入!');
              exit();

          if re.match(r'[\u4e00-\u9fff]+', cert_no):
            print('您輸入的證件號有誤!');
            continue;
          else:
            break;

      # Querying.
      final_response = QueryApi.query(pymonkey = pm, ocr = ocr, max_retries = 5, user_name = user_name, cert_no = cert_no, cert_type = choice_id_type);
      print(final_response);
      print('\r\n\r\n');
      print('==== [查詢已完成, 上方為結果, 請輸入下一條] ====')






####################################
# Init Pythonmonkey & DdddOCR.
# * Related: 
#     - Text Captcha Reader (Text_Captcha_breaker): https://huggingface.co/spaces/docparser/Text_Captcha_breaker
####################################

class HttpApiHandler(BaseHTTPRequestHandler):
  protocol_version = 'HTTP/1.1';

  def do_GET(self):
      parse_result = urlparse.urlparse(self.path);
      query_parameters = urlparse.parse_qs(parse_result.query);

      user_name = '';
      cert_no = '';
      cert_type = '';
      error = False;
      error_reason = '';

      if 'userName' in query_parameters.keys():
        if len(query_parameters['userName']) != 1:
          error = True;
        else:
          user_name = query_parameters['userName'][0];
      else:
        error = True;

      if len(user_name) == 0:
        error = True;
        error_reason = 'queryParameters userName is Empty!';


      if 'certNo' in query_parameters.keys():
        if len(query_parameters['certNo']) != 1:
          error = True;
        else:
          cert_no = query_parameters['certNo'][0];
      else:
        error = True;

      if len(cert_no) == 0:
        error = True;
        error_reason = 'queryParameters certNo is Empty!';


      if 'certType' in query_parameters.keys():
        if len(query_parameters['certType']) != 1:
          error = True;
        else:
          cert_type = query_parameters['certType'][0];
      else:
        error = True;

      if len(cert_type) == 0:
        error = True;
        error_reason = 'queryParameters certType is Empty!';

      if error:
        error_message = json.dumps({
          'errorCode': 14100,
          'exception': None,
          'reason': error_reason,
        }).encode(encoding = 'utf_8');

        self.send_response(400);
        self.send_header('Content-Type', 'application/json');
        self.send_header('Content-Length', len(error_message));
        self.send_header('Connection', 'close');
        self.end_headers();
        self.wfile.write(error_message);
        return;

      # Querying.
      query_result = QueryApi.query(pymonkey = pm, ocr = self.server.ocr, max_retries = 5, user_name = user_name, cert_no = cert_no, cert_type = cert_type);
      result_json = json.dumps(query_result).encode(encoding = 'utf-8');

      self.send_response(200);
      self.send_header('Content-Type', 'application/json');
      self.send_header('Content-Length', len(result_json));
      self.send_header('Connection', 'close');
      self.end_headers();
      self.wfile.write(result_json);




class HttpApiServer(HTTPServer):
  def __init__(self, *args, **kwargs):
    HTTPServer.__init__(self, *args, **kwargs);
    self.ocr = ddddocr.DdddOcr();
    pm.eval(FIXED_JAVASCRIPT);



def run():
  server = HttpApiServer(('0.0.0.0', 5487), HttpApiHandler);
  print('Listening on http://127.0.0.1:5487');

  try:
      server.serve_forever();
  except KeyboardInterrupt:
      print('Event: Ctrl+C !');
      exit();

if __name__ == '__main__':
    run()

# # Cli Interface.
# def main():
#   pm.eval(FIXED_JAVASCRIPT);
#   ocr = ddddocr.DdddOcr();

#   # Prompt.
#   print('\r\n\r\n');
#   print('____Zig-lang: https://ziglang.org/');
#   print('___Rust-lang: https://ziglang.org/');
#   print('Crystal-lang: https://crystal-lang.org/');
#   print('Written in November 30, 2023');
#   print('Author: @zig_rust_crystal');

#   QueryApi.cli_interface(pymonkey = pm, ocr = ocr);

# if __name__ == '__main__':
#   main();


# # Http Example
# curl --get \
#     --data-urlencode "userName=张莹莹" \
#     --data-urlencode "certNo=440303199802057227" \
#     --data-urlencode "certType=111" \
#     http://127.0.0.1:5487



    