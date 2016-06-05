String.format = function() {
    if( arguments.length == 0 )
        return null;

    var str = arguments[0]; 
    for(var i=1;i<arguments.length;i++) {
        var re = new RegExp('\\{' + (i-1) + '\\}','gm');
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
    getStoreName: function (store) {
        if (store.name) {
            return store.name;
        } else {
            return "匿名("+store.id+")";
        }
    },
    getStoreAvatar: function (store) {
        if (store.avatar) {
            var parser = document.createElement('a');
            parser.href = user.avatar;
            return parser.pathname;
        } else {
            return '';
        }
    }
};

var htmlLoyout = {
    buildStore: function (store) {
        var html = [];
        var s;

        s = String.format('<li  data-id="{0}">',store.id);
        html.push(s);
        if (store.avatar) {
            html.push('    <img src="' + helper.getStoreAvatar(user) + '" class="avatar" alt=""/>');
        } else {
            html.push('    <img src="/static/images/kfl.png" class="avatar" alt=""/>');
        }
        if (helper.getStoreName(store)) {
            html.push('    <span class="name">' + helper.getStoreName(store) + '</span>');
        }
        html.push('    <span class="num">' + (store.num || '') + '</span>');
        html.push('</li>');
        return html.join('');
    },
    buildText: function (msg) {
        var html = [];
        html.push('<li class="chat-item" data-id="' + msg.id + '">');
		if(msg.cls=='message-out'){
		html.push('<div style="float:right;margin-left:20px"><img src="/static/images/_avatar.png" width="50px"></div>');
		}else if(msg.cls=='message-in'){
		html.push('<div style="float:left;margin-right:20px"><img src="/static/images/kfl.png" width="50px"></div>');
		}
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
        var html = [];
        html.push('<li class="chat-item"  data-id="' + msg.id + '">');
        html.push('    <div class="message">');
        html.push('        <div class="bubble"><p class="pre"><a href="' + msg.image + '" target="_blank">' +
            '<img class="image-thumb-body" src="' + msg.image + '" /></p></a>');
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
    }
};
var node = {
    chatHistory: $("#chatHistory ul"),
    usersList: $('#usersList'),
    exit: $('#exit')
};
var process = {
    playAudio: function () {

    },
    appendAudio: function (m) {
        node.chatHistory.append(htmlLoyout.buildAudio(m));
    },
    appendText: function (m) {
        node.chatHistory.append(htmlLoyout.buildText(m));
    },
    appendImage: function (m) {
        node.chatHistory.append(htmlLoyout.buildImage(m));
    },
    msgTip: function (storeID) {
        var userDom = node.usersList.find('li[data-id="' + storeID + '"]'),
            num = '';
        if (userDom) {
            num = userDom.find('.num').text();
            if (!userDom.hasClass('active')) {
                if (num) {
                    num++;
                } else {
                    num = 1;
                }
                userDom.find('.num').text(num);
            }
            node.usersList.prepend(userDom);
        }
    },
    msgACK: function (msgID) {
        node.chatHistory.find('li[data-id="' + msgID + '"] .bubble').append(htmlLoyout.buildACK());
    }
};

function scrollDown() {
    $('#chatHistory').scrollTop($('#chatHistory ul').outerHeight());
    $("#entry").text('').focus();
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

// add message on board
function addMessage(msg) {
    appendMessage(msg);
    scrollDown();
}

function addStore(store) {
    node.usersList.prepend(htmlLoyout.buildStore(store));
}

function setUserName(storeID, name) {
    var userDom = node.usersList.find('li[data-id="' + storeID + '"]');
    if (userDom) {
        userDom.find('.name').text(name);
    }
}

function setName(username) {
    $("#name").text(username);
}

function showChat() {
    $("#chat").removeClass('hide').show();
    scrollDown();
}

$(document).ready(function () {
    r = util.getURLParameter('uid', location.search);
    if (r) {
        uid = parseInt(r);
    }

    r = util.getURLParameter('appid', location.search);
    if (r) {
        appID = parseInt(r);
    }

    var token = "";
    r = util.getURLParameter('token', location.search);
    if (r) {
        token = r;
    }

    var name = "";
    r = util.getURLParameter('name', location.search);
    if (r) {
        name = r;
    }

    console.log("appid:", appID);
    console.log("uid:", uid);
    console.log("token:" + token);
    console.log("name:", name);

    loginUser.name = name;
    loginUser.uid = uid;
    loginUser.appID = appID;
    loginUser.accessToken = token;
    loginUser.storeID = storeID;

    im.accessToken = loginUser.accessToken;
    if (host) {
        im.host = host;
    }
    im.start();

    if (loginUser.name) {
        setName(loginUser.name);
    }
    showChat();

    node.usersList.on('click', 'li', function () {
        var _this = $(this),
            store_id = _this.attr('data-id'),
            main = $('#main');

        if (store_id == storeID) {
            return;
        }

        $('#intro').hide();
        $('#to_user').attr('data-id', store_id);

        store = storeDB.findStore(store_id);
        if (store) {
            $('#to_user').text(helper.getStoreName(store));
        }

        if (store.avatar) {
            $('#to_user_avatar').attr("src", helper.getStoreAvatar(store));
        } else {
            var defaultAvatar = "/static/images/img-default.png";
            $('#to_user_avatar').attr("src", defaultAvatar);
        }

        main.find('.chat-wrap').removeClass('hide');
        _this.addClass('active').siblings().removeClass('active');
        _this.find('.num').text('');
        ///读取聊天记录添加到列表
        var messages = imDB.loadUserMessage(store_id);
        node.chatHistory.html("");
        for (var i in messages) {
            var msg = messages[i];
            console.log("message:", msg);
            appendMessage(msg);
            sellerID = msg.sellerID;
        }
        storeID = store_id;
    });

    //deal with chat mode.
    $("#entry").keypress(function (e) {
        if (e.keyCode != 13) return;
        var msg = $("#entry").val().replace("\n", "");
        if (!util.isBlank(msg)) {
            var now = new Date();
            var obj = {"text": msg};
            var textMsg = JSON.stringify(obj);
            console.log("message text:", textMsg);
            var message = {
                sellerID: sellerID,
                storeID: storeID,
                customerID: loginUser.uid,
                customerAppID: loginUser.appID,
                content: textMsg,
                msgLocalID: msgLocalID++,
                outgoing: true,
                timestamp: (now.getTime() / 1000)
            };
            message.contentObj = obj;
            if (im.connectState == IMService.STATE_CONNECTED) {
                imDB.saveMessage(message.storeID, message);

                console.log("send message:", message);
                im.sendCustomerMessage(message);
                $("#entry").val(""); // clear the entry field.
                addMessage(message);
                $("#chatHistory").show();
            }
        }
        return false;
    });

    var MSG_CUSTOMER = 24;
    var MSG_CUSTOMER_SUPPORT = 25;

    var url =  apiURL + "/messages";
    $.ajax({
        url: url,
        dataType: 'json',
        headers: {"Authorization": "Bearer " + token},
        success: function (result, status, xhr) {
            console.log("messges:", result);
            if (!result) {
                return;
            }
            msgs = result.data

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
                    messageObserver.handleCustomerMessage(msg);
                    messageObserver.handleCustomerMessageACK(msg);
                } else if (m['command'] == MSG_CUSTOMER_SUPPORT) {
                    msg.content = m['content'];
                    msg.customerAppID = m['customer_appid'];
                    msg.customerID = m['customer_id'];
                    msg.storeID = m['store_id'];
                    msg.sellerID = m['seller_id'];
                    msg.timestamp = m['timestamp'];
                    msg.msgLocalID = msgLocalID++;
                    messageObserver.handleCustomerSupportMessage(msg, false);
                }
            }
        },
        error: function (xhr, err) {
            console.log("get customer name err:", err, xhr.status);
        }
    });

});




