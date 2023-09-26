function scrollToNewMessage() {
  // get the message body 
  var chatBody = document.querySelector(".chat-history-body");
  
  // scroll to the newest message
  chatBody.scrollTo(0, chatBody.scrollHeight);
}

function renderUserChats(userChatsObject){
  // debug
  // console.log(userChatsObject);

  // extract the major data points
  var userName = userChatsObject.name;

  var userEmail = userChatsObject.email;

  // create the avatar node
  if (userChatsObject.avatar === "missing"){
    // get the initials
    var userNameInitials = userChatsObject.initials;

    var avatarNode = `
                    <div class="avatar me-2">
                      <span class="avatar-initial rounded-circle bg-label-success">
                          ${userNameInitials}
                      </span>
                    </div>
                    `;

  } else{
    // get the image url
    var imageUrl = userChatsObject.avatar;

    var avatarNode = `
                  <div class="avatar avatar-sm">
                    <img src="${imageUrl}" alt="Avatar" class="rounded-circle">
                  </div>
                    `;

  }

  // load the info

  // username
  document.getElementById("user-name-holder").innerHTML = userName;

  // username attribute
  document.getElementById("user-name-holder").setAttribute("data-user-name", userName)

  // email
  document.getElementById("user-email-holder").innerHTML = userEmail;

  // avatar
  document.getElementById("avatar-showcase").innerHTML = avatarNode;

  // access the chats
  var presentChats = userChatsObject.chats;

  // wipe the chats holder
  if (presentChats.length > 0){
    // load the chats
    var chatsHolder = document.getElementById("chats-holder-container");

    // clean the display
    chatsHolder.innerHTML = "";

    presentChats.forEach(chatObject => {
      // {'time': '04-09-2023, 11:17 AM', 'message': 'hope all is well', 'userGroup': 2},
      // get the details
      var timeObject = chatObject.time;

      var messageObject = chatObject.message;

      var userGroup = chatObject.userGroup;

      // console.log(timeObject, messageObject, userGroup);

      // create parent node
      var chatParentNode = document.createElement('li');

        // add default class
        chatParentNode.classList.add("chat-message");

      if (userGroup === 2){
        // var 
        var displayNode = `
                        <div class="d-flex overflow-hidden">

                          ${avatarNode}

                          <div class="chat-message-wrapper flex-grow-1">
                            <div class="chat-message-text">
                                <p class="mb-0">${messageObject}</p>
                            </div>
                            <div class="text-muted mt-1">
                                <small>${timeObject}</small>
                            </div>
                          </div>
                        </div>`;
      } else {
        // add right display styles
        chatParentNode.classList.add("chat-message-right");

        var displayNode = `
                          <div class="d-flex overflow-hidden">
                              <div class="chat-message-wrapper flex-grow-1">
                              <div class="chat-message-text">
                                  <p class="mb-0">${messageObject}</p>
                              </div>
                              <div class="text-end text-muted mt-1">
                                  <i class='bx bx-check-double text-success d-none'></i>
                                  <small>${timeObject}</small>
                              </div>
                              </div>

                              <div class="avatar ms-3">
                                  <span class="avatar-initial rounded-circle bg-label-info">
                                      <i class="bx bx-support"></i>
                                  </span>
                              </div>
                          </div>`;
      }

      // display the nodes
      chatParentNode.innerHTML = displayNode;

      // add the node to the list
      chatsHolder.appendChild(chatParentNode);


    });

  } else {
    // wipe the interface
    document.getElementById("chats-holder-container").innerHTML = "";

  }

  // scroll to last message
  if (presentChats.length > 0){
    scrollToNewMessage();
  } else {

  }


}

function fetchAndUpdateChats(userNameToGet, validityToken){
  // create a form
  var newForm = new FormData();

  // send user name
  newForm.append("user-name", userNameToGet);


  // prepare to send
  var xmlHttpRequest = new XMLHttpRequest();

  // bridge to the server
  xmlHttpRequest.open("POST", "/get-user-chats/");

  // add the validation headers
  xmlHttpRequest.setRequestHeader("X-CSRFToken", validityToken);

  // alert that json is expected
  xmlHttpRequest.setRequestHeader("Accept", "application/json");

  // track changes
  xmlHttpRequest.onload = ()=>{
      if (xmlHttpRequest.status == 200){
          // get the response
          var responseData = JSON.parse(xmlHttpRequest.responseText);

          // console.log(responseData);

          // display the information
          renderUserChats(responseData.message);


      } else {
          // alert network issues
          // statusShowLabel.innerHTML = "No Internet connection detected, please try again";
          console.log('Connection failed');
      }
  };

  // send
  xmlHttpRequest.send(newForm);

}


"use strict";
document.addEventListener("DOMContentLoaded", function () {
  {
    const o = document.querySelector(".app-chat-contacts .sidebar-body"),
      n = [].slice.call(
        document.querySelectorAll(
          ".chat-contact-list-item:not(.chat-contact-list-item-title)"
        )
      ),
      i = document.querySelector(".chat-history-body"),
      u = document.querySelector(".app-chat-sidebar-left .sidebar-body"),
      d = document.querySelector(".app-chat-sidebar-right .sidebar-body"),
      h = [].slice.call(
        document.querySelectorAll(".form-check-input[name='chat-user-status']")
      ),
      m = $(".chat-sidebar-left-user-about"),
      f = document.querySelector(".chat-search-input"),
      b = $(".speech-to-text"),
      y = {
        active: "avatar-online",
        offline: "avatar-offline",
        away: "avatar-away",
        busy: "avatar-busy",
      };
    function a() {
      if (i){
        i.scrollTo(0, i.scrollHeight);
      }
      
    }

    function l(e, a, c, t) {
      e.forEach((e) => {
        var t = e.textContent.toLowerCase();
        !c || -1 < t.indexOf(c)
          ? (e.classList.add("d-flex"), e.classList.remove("d-none"), a++)
          : e.classList.add("d-none");
      }),
        0 == a ? t.classList.remove("d-none") : t.classList.add("d-none");
    }
    o && new PerfectScrollbar(o, { wheelPropagation: !1, suppressScrollX: !0 }),
      i &&
        new PerfectScrollbar(i, { wheelPropagation: !1, suppressScrollX: !0 }),
      u &&
        new PerfectScrollbar(u, { wheelPropagation: !1, suppressScrollX: !0 }),
      d &&
        new PerfectScrollbar(d, { wheelPropagation: !1, suppressScrollX: !0 }),
      a(),
      m.length &&
        m.maxlength({
          alwaysShow: !0,
          warningClass: "label label-success bg-success text-white",
          limitReachedClass: "label label-danger",
          separator: "/",
          validate: !0,
          threshold: 120,
        }),
      h.forEach((e) => {
        e.addEventListener("click", (e) => {
          var t = document.querySelector(".chat-sidebar-left-user .avatar"),
            e = e.currentTarget.value,
            t =
              (t.removeAttribute("class"),
              Helpers._addClass("avatar avatar-xl " + y[e], t),
              document.querySelector(".app-chat-contacts .avatar"));
          t.removeAttribute("class"),
            Helpers._addClass("flex-shrink-0 avatar " + y[e] + " me-3", t);
        });
      }),
      n.forEach((e) => {
        e.addEventListener("click", (e) => {
          n.forEach((e) => {
            e.classList.remove("active");
          }),
            // add the active class
            e.currentTarget.classList.add("active"),

            // get the selected user name
            userNameSelected = e.currentTarget.querySelector("h6.chat-contact-name").getAttribute("data-receiver-name"),

            validationToken = e.currentTarget.querySelector("form#fetch-form").querySelector("input[name='csrfmiddlewaretoken']").value;

            // get the chats for that person
            fetchAndUpdateChats(userNameSelected, validationToken);

        });
      }),
      f &&
        f.addEventListener("keyup", (e) => {
          var e = e.currentTarget.value.toLowerCase(),
            t = document.querySelector(".chat-list-item-0"),
            a = document.querySelector(".contact-list-item-0"),
            c = [].slice.call(
              document.querySelectorAll(
                "#chat-list li:not(.chat-contact-list-item-title)"
              )
            ),
            r = [].slice.call(
              document.querySelectorAll(
                "#contact-list li:not(.chat-contact-list-item-title)"
              )
            );
          l(c, 0, e, t), l(r, 0, e, a);
        });
        
    let e = document.querySelector(
        ".chat-history-header [data-target='#app-chat-contacts']"
      )
    var c, r, s;
      b.length &&
        null != (c = c || webkitSpeechRecognition) &&
        ((r = new c()),
        (s = !1),
        b.on("click", function () {
          const t = $(this);
          !(r.onspeechstart = function () {
            s = !0;
          }) === s && r.start(),
            (r.onerror = function (e) {
              s = !1;
            }),
            (r.onresult = function (e) {
              t.closest(".form-send-message")
                .find(".message-input")
                .val(e.results[0][0].transcript);
            }),
            (r.onspeechend = function (e) {
              (s = !1), r.stop();
            });
        }));
  }
});
