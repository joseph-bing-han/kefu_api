var msgLocalID = 0;

var sellerID = 0;
var appID = 0;
var uid = 0;
var token = "";

String.format = function () {
    if (arguments.length == 0)
        return null;

    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
};

var helper = {
    toTime: function (ts) {
        //时间戳取时间
        var d = ts ? new Date(ts) : new Date();
        var H = d.getHours();
        var m = d.getMinutes();
        return H + ':' + (m < 10 ? '0' + m : m);
    },
    getUserName: function (user) {
        if (user.name) {
            return user.name;
        } else {
            return "匿名(" + user.uid + ")";
        }
    },
    getUserAvatar: function (user) {
        if (user.avatar) {
            var parser = document.createElement('a');
            parser.href = user.avatar;
            return parser.pathname;
        } else {
            return '';
        }
    },
};

var htmlLoyout = {
    buildText: function (msg) {
        var html = [];
        html.push('<li class="chat-item" data-id="' + msg.id + '">');
        html.push('    <div class="message ' + msg.cls + '">');
        html.push('        <div class="bubble"><p class="pre">' + msg.text + '</p>');
        html.push('           <span class="time">' + helper.toTime(msg.timestamp * 1000) + '</span>');

        if (msg.ack) {
            html.push('   <span class="ack"></span>');
        }

        html.push('        </div>');
        html.push('    </div>');
        html.push('</li>');
        return html.join('');
    },
    buildImage: function (msg) {
        console.log('msg====', msg)
        var html = [];
        html.push('<li class="chat-item"  data-id="' + msg.id + '">');
        html.push('    <div class="message ' + msg.cls + '">');
        html.push('        <div class="bubble">' +
            '<img class="image-thumb-body" src="' + msg.image + '" /><br /><br />');
        html.push('           <span class="time">' + helper.toTime(msg.timestamp * 1000) + '</span>');

        if (msg.ack) {
            html.push('   <span class="ack"></span>');
        }

        html.push('        </div>');
        html.push('    </div>');
        html.push('</li>');
        return html.join('');
    },
    buildAudio: function (msg) {
        var html = [];
        html.push('<li class="chat-item"  data-id="' + msg.id + '">');
        var audio_url = msg.audio.url + ".mp3";
        html.push('<li class="chat-item">');
        html.push('  <div class="message ' + msg.cls + '">');
        html.push('     <div class="bubble">');
        html.push('       <p class="pre"><audio  controls="controls" src="' + audio_url + '"></audio></p>');
        html.push('       <span class="time">' + helper.toTime(msg.timestamp * 1000) + '</span>');

        if (msg.ack) {
            html.push('   <span class="ack"></span>');
        }

        html.push('     </div>');
        html.push('  </div>');
        html.push('</li>');
        return html.join('');
    },
    buildACK: function () {
        return '<span class="ack"></span>';
    },
};

var dom = {

    chatHistory: $("#chatHistory ul"),
    entry: $("#entry")
};

var process = {
    playAudio: function () {

    },
    appendAudio: function (m) {
        dom.chatHistory.append(htmlLoyout.buildAudio(m));
    },
    appendText: function (m) {
        dom.chatHistory.append(htmlLoyout.buildText(m));
    },
    appendImage: function (m) {
        dom.chatHistory.append(htmlLoyout.buildImage(m));
    },
    msgACK: function (msgID) {
        dom.chatHistory.find('li[data-id="' + msgID + '"] .bubble').append(htmlLoyout.buildACK());
    }
};

function scrollDown() {
    $(document.body).scrollTop($(document.body).outerHeight());
}
function checkGoBottom() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 300) {
        scrollDown();
    } else {
        var newTip = $('#new_tip');
        if (!newTip.hasClass('show')) {
            newTip.addClass('show');
            setTimeout(function () {
                newTip.removeClass('show');
            }, 3000)
        }
    }
}

function appendMessage(msg) {
    var time = new Date();
    var m = {};
    m.id = msg.msgLocalID;
    if (msg.timestamp) {
        time.setTime(msg.timestamp * 1000);
        m.timestamp = msg.timestamp;
    }
    m.ack = msg.ack;

    if (msg.outgoing) {
        m.cls = "message-out";
    } else {
        m.cls = "message-in";
    }
    if (msg.contentObj.text) {
        m.text = util.toStaticHTML(msg.contentObj.text);
        process.appendText(m);
    } else if (msg.contentObj.audio) {
        m.audio = msg.contentObj.audio;
        process.appendAudio(m);
    } else if (msg.contentObj.image) {
        m.image = msg.contentObj.image;
        process.appendImage(m);
    }
}

observer = {
    handleCustomerMessage: function (msg) {
        if (msg.customerID != uid || msg.customerAppID != appID) {
            return;
        }
        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }

        sellerID = msg.sellerID;
        msg.outgoing = true;
        msg.msgLocalID = msgLocalID++;
        appendMessage(msg);
    },
    handleCustomerSupportMessage: function (msg, hideTip) {
        if (msg.customerID != uid || msg.customerAppID != appID) {
            return;
        }
        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }

        sellerID = msg.sellerID;
        msg.outgoing = false;
        msg.msgLocalID = msgLocalID++;
        appendMessage(msg);
        if (!hideTip) { //非首次加载
            checkGoBottom();
            window.localStorage.setItem('lastMsg', window.JSON.stringify(msg));
        }

    },
    handleCustomerMessageACK: function (msg) {
        console.log("handleCustomerMessageACK...");
        var msgLocalID = msg.msgLocalID;
        process.msgACK(msgLocalID);
    },
    handleCustomerMessageFailure: function (msg) {
        console.log("handleCustomerMessageFailure...");
    },

    onConnectState: function (state) {
        if (state == IMService.STATE_CONNECTED) {
            console.log("im connected");
        } else if (state == IMService.STATE_CONNECTING) {
            console.log("im connecting");
        } else if (state == IMService.STATE_CONNECTFAIL) {
            console.log("im connect fail");
        } else if (state == IMService.STATE_UNCONNECTED) {
            console.log("im unconnected");
        }
    }
};

var im = new IMService(observer);


$(document).ready(function () {
    var r = util.getURLParameter('store', location.search);
    if (r) {
        storeID = parseInt(r);
    }

    r = util.getURLParameter('uid', location.search);
    if (r) {
        uid = parseInt(r);
    } else if (customerID) {
        uid = customerID;
    }

    r = util.getURLParameter('appid', location.search);
    if (r) {
        appID = parseInt(r);
    } else if (customerAppID) {
        appID = customerAppID;
    }

    token = "";
    r = util.getURLParameter('token', location.search);
    if (r) {
        token = r;
    } else if (customerToken) {
        token = customerToken;
    }
    console.log("appid:", appID);
    console.log("uid:", uid);
    console.log("store id:", storeID);
    console.log("token:" + token);


    if (!token || !appID || !uid || !storeID) {
        return;
    }

    if (host) {
        im.host = host;
    }
    im.accessToken = token
    im.start();

    function sendMsg() {
        var msg = $("#entry").val().replace("\n", "");
        if (!util.isBlank(msg)) {
            var now = new Date();
            var obj = {"text": msg};
            var textMsg = JSON.stringify(obj);
            var message = {
                customerID: uid,
                customerAppID: appID,
                storeID: storeID,
                sellerID: sellerID,
                content: textMsg,
                contentObj: obj,
                msgLocalID: msgLocalID++
            };
            message.outgoing = true;
            message.timestamp = (now.getTime() / 1000);

            if (im.connectState == IMService.STATE_CONNECTED) {
                im.sendCustomerMessage(message);
                $("#entry").val("").blur();
                appendMessage(message);
            }
            scrollDown();
        }
    }

    $('#chat_button').on('click', function () {
        sendMsg();
    });


    dom.entry.keypress(function (e) {
        if (e.keyCode != 13) return;
        e.stopPropagation();
        e.preventDefault();
        sendMsg()
    });
    dom.entry.on('touchstart', function () {
        scrollDown();
    });

    var MSG_CUSTOMER = 24;
    var MSG_CUSTOMER_SUPPORT = 25;

    var url = apiURL + "/messages?store=" + storeID;
    $.ajax({
        url: url,
        dataType: 'json',
        headers: {"Authorization": "Bearer " + token},
        success: function (result, status, xhr) {
            console.log("messges:", result);
            if (!result) {
                return;
            }
            var msgs = result.data

            for (var i = 0; i < msgs.length; i++) {
                var msg = {};
                var m = msgs[i];
                console.log("msg command:", m['command']);
                if (m['command'] == MSG_CUSTOMER) {
                    msg.content = m['content'];
                    msg.customerAppID = m['customer_appid'];
                    msg.customerID = m['customer_id'];
                    msg.storeID = m['store_id'];
                    msg.sellerID = m['seller_id'];
                    msg.timestamp = m['timestamp'];
                    msg.msgLocalID = msgLocalID++;
                    observer.handleCustomerMessage(msg);
                    observer.handleCustomerMessageACK(msg);
                } else if (m['command'] == MSG_CUSTOMER_SUPPORT) {
                    msg.content = m['content'];
                    msg.customerAppID = m['customer_appid'];
                    msg.customerID = m['customer_id'];
                    msg.storeID = m['store_id'];
                    msg.sellerID = m['seller_id'];
                    msg.timestamp = m['timestamp'];
                    msg.msgLocalID = msgLocalID++;
                    observer.handleCustomerSupportMessage(msg, true);
                }
            }
            setTimeout(function () {
                scrollDown();
            }, 500)
        },
        error: function (xhr, err) {
            console.log("get customer name err:", err, xhr.status);
        }
    });

    $('#chatHistory').on('click', '.image-thumb-body', function () {
        var _this = $(this);
        var src = _this.attr('src');
        $(document.body).append('<div class="open-img-wrap"><img src="' + src + '" class="open-img" /></div>')
    });
    $(document.body).on('click', '.open-img-wrap', function () {
        $(this).remove();
    });

    var lastMsg = window.localStorage.getItem('lastMsg');
    if (lastMsg) {
        lastMsg = window.JSON.parse(lastMsg);
        alert(window.JSON.parse(lastMsg.content)['text']);

    }


    $(window).on('unload', function () {
        console.log('unload');
        im.stop();
        return false
    });

});
