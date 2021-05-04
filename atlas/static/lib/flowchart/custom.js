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
function loadFlowcharts() {
  var d = document,
    m = d.getElementsByClassName("mermaid");
  [].forEach.call(m, function (e) {
    if (e.getElementsByTagName("svg").length == 0) {
      var t = document.createElement("textarea");
      t.innerHTML = e.innerHTML;
      var chart,
        code = t.value;
      e.innerHTML = "";
      t = null;
      if (code.trim() != "") {
        try {
          chart = flowchart.parse(code);
          chart.drawSVG(e);
        } catch (l) {}
      }
    }
  });
}

loadFlowcharts();

document.addEventListener("load-charts", function () {
  setTimeout(function () {
    loadFlowcharts();
  }, 0);
});
