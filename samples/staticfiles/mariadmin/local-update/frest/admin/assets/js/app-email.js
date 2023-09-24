function deleteAssociatedDataAndEntries(userName, userEmail, validationToken){
    // create a form
    var newForm = new FormData();

    // add the message to the form
    newForm.append("user-name", userName);

    newForm.append('user-email', userEmail);

    // prepare to send
    var xmlHttpRequest = new XMLHttpRequest();

    // bridge to the server
    xmlHttpRequest.open("POST", "/delete-thread/");

    // add the validation headers
    xmlHttpRequest.setRequestHeader("X-CSRFToken", validationToken);

    xmlHttpRequest.setRequestHeader("Accept", "application/json");

    // track changes
    xmlHttpRequest.onload = ()=>{
        if (xmlHttpRequest.status == 200){
          // get json
          var jsonResponse = JSON.parse(xmlHttpRequest.responseText);

          // update the labels
          document.getElementById("inbox-count-show").innerHTML = jsonResponse.inbox;

          document.getElementById("user-count-show").innerHTML = jsonResponse.holder;


          // console.log("updated");



        } else {
            // console.log('Connection failed');
        }
    };

    // send
    xmlHttpRequest.send(newForm);



}

"use strict";
document.addEventListener("DOMContentLoaded", function () {
  {
    const r = document.querySelector(".email-list"),
      o = [].slice.call(document.querySelectorAll(".email-list-item")),
      i = [].slice.call(document.querySelectorAll(".email-list-item-input")),
      s = document.querySelector(".app-email-view-content"),
      c = document.querySelector(".email-filters"),
      n = [].slice.call(document.querySelectorAll(".email-filter-folders li")),
      d = document.querySelector(".email-editor"),
      m = document.querySelector(".app-email-sidebar"),
      u = document.querySelector(".app-overlay"),
      p = document.querySelector(".email-reply-editor"),
      v = [].slice.call(document.querySelectorAll(".email-list-item-bookmark")),
      g = document.getElementById("email-select-all"),
      h = document.querySelector(".email-search-input"),
      S = document.querySelector(".email-compose-toggle-cc"),
      y = document.querySelector(".email-compose-toggle-bcc"),
      b = document.querySelector(".email-list-delete"),
      f = document.querySelector(".email-list-read"),
      L = document.querySelector(".email-refresh"),
      q = document.getElementById("app-email-view"),
      E = [].slice.call(document.querySelectorAll(".email-filter-folders li")),
      w = [].slice.call(
        document.querySelectorAll(".email-list-item-actions li")
      );
    if (
      (r &&
        new PerfectScrollbar(r, { wheelPropagation: !1, suppressScrollX: !0 }),
      c &&
        new PerfectScrollbar(c, { wheelPropagation: !1, suppressScrollX: !0 }),
      s &&
        new PerfectScrollbar(s, { wheelPropagation: !1, suppressScrollX: !0 }),
        v.forEach((e) => {
          e.addEventListener("click", (e) => {
            var t = e.currentTarget.parentNode.parentNode,
              l = t.getAttribute("data-starred");
            e.stopPropagation(),
              l
                ? t.removeAttribute("data-starred")
                : t.setAttribute("data-starred", "true");
          });
        }),
      g &&
        g.addEventListener("click", (e) => {
          e.currentTarget.checked
            ? i.forEach((e) => (e.checked = 1))
            : i.forEach((e) => (e.checked = 0));
        }),
      i &&
        i.forEach((e) => {
          e.addEventListener("click", (e) => {
            e.stopPropagation();
            let t = 0;
            i.forEach((e) => {
              e.checked && t++;
            }),
              t < i.length
                ? 0 == t
                  ? (g.indeterminate = !1)
                  : (g.indeterminate = !0)
                : t == i.length
                ? ((g.indeterminate = !1), (g.checked = !0))
                : (g.indeterminate = !1);
          });
        }),
      h &&
        h.addEventListener("keyup", (e) => {
          let l = e.currentTarget.value.toLowerCase(),
            t = {},
            a = document
              .querySelector(".email-filter-folders .active")
              .getAttribute("data-target");
          (t =
            "inbox" != a
              ? [].slice.call(
                  document.querySelectorAll(
                    ".email-list-item[data-" + a + '="true"]'
                  )
                )
              : [].slice.call(
                  document.querySelectorAll(".email-list-item")
                )).forEach((e) => {
            var t = e.textContent.toLowerCase();
            l
              ? -1 < t.indexOf(l)
                ? e.classList.add("d-block")
                : e.classList.add("d-none")
              : e.classList.remove("d-none");
          });
        }),
      n.forEach((e) => {
        e.addEventListener("click", (e) => {
          let t = e.currentTarget,
            l = t.getAttribute("data-target");

            // hide any side bar penry
            m.classList.remove("show"),

            // remove the overlay
            u.classList.remove("show"),

            // remove the active class from others
            Helpers._removeClass("active", n),

            // make it the current active element
            t.classList.add("active"),

            

            o.forEach((e) => {
              "inbox" == l || e.hasAttribute("data-" + l)
                ? (e.classList.add("d-block"), e.classList.remove("d-none"))
                : (e.classList.add("d-none"), e.classList.remove("d-block"));
            });
        });
      }),
      y &&
        y.addEventListener("click", (e) => {
          Helpers._toggleClass(
            document.querySelector(".email-compose-bcc"),
            "d-block",
            "d-none"
          );
        }),
      S &&
        S.addEventListener("click", (e) => {
          Helpers._toggleClass(
            document.querySelector(".email-compose-cc"),
            "d-block",
            "d-none"
          );
        }),
      b &&
        b.addEventListener("click", (e) => {
          i.forEach((e) => {
            // delete each checked email entry
            if (e.checked){
              // delete the attached email objects
              var emailNodeParent = e.parentNode.closest("li.email-list-item");

              // get the name and email of the user
              var selectedEmailAddress = emailNodeParent.getAttribute("data-attached-email");

              var selectedUserName = emailNodeParent.getAttribute("data-attached-user");

              // get the validity token
              var validityToken = document.getElementById(selectedUserName).querySelector('input[name="csrfmiddlewaretoken"]').value;

              // delete all details associated with such users
              deleteAssociatedDataAndEntries(selectedUserName, selectedEmailAddress, validityToken);

              // console.log("Validity Token:", validityToken);
              
              
              // remove it at last
              emailNodeParent.remove();

            } else {

            }
          }),
            (g.indeterminate = !1),
            (g.checked = !1);
        }),
      f &&
        f.addEventListener("click", (e) => {
          i.forEach((e) => {
            e.checked &&
              ((e.checked = !1),
              e.parentNode
                .closest("li.email-list-item")
                .classList.add("email-marked-read"),
              (e = e.parentNode
                .closest("li.email-list-item")
                .querySelector(".email-list-item-actions li")),
              Helpers._hasClass("email-read", e) &&
                (e.classList.remove("email-read"),
                e.classList.add("email-unread"),
                e.querySelector("i").classList.remove("bx-envelope-open"),
                e.querySelector("i").classList.add("bx-envelope")));
          }),
            (g.indeterminate = !1),
            (g.checked = !1);
        }),
      L && r)
    ) {
      let t = $(".email-list"),
        l = new PerfectScrollbar(r, {
          wheelPropagation: !1,
          suppressScrollX: !0,
        });
      L.addEventListener("click", (e) => {
        t.block({
          message:
            '<div class="spinner-border text-primary" role="status"></div>',
          timeout: 1e3,
          css: { backgroundColor: "transparent", border: "0" },
          overlayCSS: { backgroundColor: "#000", opacity: 0.1 },
          onBlock: function () {
            l.settings.suppressScrollY = !0;
          },
          onUnblock: function () {
            l.settings.suppressScrollY = !1;
          },
        });
      });
    }
    var l = $(".email-earlier-msgs");
    l.length &&
      l.on("click", function () {
        var e = $(this);
        e.parents().find(".email-card-last").addClass("hide-pseudo"),
          e.next(".email-card-prev").slideToggle(),
          e.remove();
      });
    let t = $("#emailContacts");
    function a() {
      function e(e) {
        return e.id
          ? "<div class='d-flex flex-wrap align-items-center'><div class='avatar avatar-xs me-2'><img src='" +
              assetsPath +
              "img/avatars/" +
              $(e.element).data("avatar") +
              "' alt='avatar' class='rounded-circle' /></div>" +
              e.text +
              "</div>"
          : e.text;
      }
      t.length &&
        t.wrap('<div class="position-relative"></div>').select2({
          placeholder: "Select value",
          dropdownParent: t.parent(),
          closeOnSelect: !1,
          templateResult: e,
          templateSelection: e,
          escapeMarkup: function (e) {
            return e;
          },
        });
    }
    a();
    let e = $(".app-email-view-content");
    e.find(".scroll-to-reply").on("click", function () {
      0 === e[0].scrollTop && e.animate({ scrollTop: e[0].scrollHeight }, 1500);
    }),
      E &&
        E.forEach((e) => {
          e.addEventListener("click", (e) => {
            q.classList.remove("show");
          });
        }),
      w &&
        w.forEach((e) => {
          e.addEventListener("click", (e) => {
            e.stopPropagation();
            e = e.currentTarget;
            Helpers._hasClass("email-delete", e)
              ? e.parentNode.closest("li.email-list-item").remove()
              : Helpers._hasClass("email-read", e)
              ? (e.parentNode
                  .closest("li.email-list-item")
                  .classList.add("email-marked-read"),
                Helpers._toggleClass(e, "email-read", "email-unread"),
                Helpers._toggleClass(
                  e.querySelector("i"),
                  "bx-envelope-open",
                  "bx-envelope"
                ))
              : Helpers._hasClass("email-unread", e) &&
                (e.parentNode
                  .closest("li.email-list-item")
                  .classList.remove("email-marked-read"),
                Helpers._toggleClass(e, "email-read", "email-unread"),
                Helpers._toggleClass(
                  e.querySelector("i"),
                  "bx-envelope-open",
                  "bx-envelope"
                ));
          });
        });
  }
});
