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
    getUserName: function (user) {
        if (user.name) {
            return user.name;
        } else {
            return "匿名("+user.uid+")";
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
    buildUser: function (user) {
        var html = [];
        var s;
        var cid = "" + user.appid + ":" + user.uid;

        s = String.format('<li data-uid="{0}" data-appid="{1}" data-id="{2}">',
                          user.uid, user.appid,  cid);
        html.push(s);
        if (user.avatar) {
            html.push('    <img src="' + helper.getUserAvatar(user) + '" class="avatar" alt=""/>');
        } else {
            html.push('    <img src="static/images/_avatar.png" class="avatar" alt=""/>');
        }
        if (helper.getUserName(user)) {
            html.push('    <span class="name">' + helper.getUserName(user) + '</span>');
        }else{
            html.push('    <span class="uid">' + helper.getPhone(user.uid) + '</span>');
        }
        html.push('    <span class="num">' + (user.num || '') + '</span>');
        html.push('</li>');
        return html.join('');
    },
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
    },
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
    msgTip: function (appid, uid) {
        var cid = "" + appid + ":" + uid;
        var userDom = node.usersList.find('li[data-id="' + cid + '"]'),
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
    },
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

// show tip
function tip(type, name) {
    var tip, title;
    switch (type) {
        case 'online':
            tip = name + ' is online now.';
            title = 'Online Notify';
            break;
        case 'offline':
            tip = name + ' is offline now.';
            title = 'Offline Notify';
            break;
        case 'message':
            tip = name + ' is saying now.';
            title = 'Message Notify';
            break;
    }
    var pop = new Pop(title, tip);
}

function addUser(user) {
    node.usersList.prepend(htmlLoyout.buildUser(user));
}


function setName(username) {
    $("#name").text(username);
}

function showChat() {
    $("#chat").removeClass('hide').show();
    scrollDown();
}

$(document).ready(function () {
    var token = util.getCookie("token");
    var uid = util.getCookie("uid");
    var storeID = util.getCookie("store_id");
    storeID = parseInt(storeID);

    console.log("token:", token);
    console.log("uid:", uid);
    console.log("storeID", storeID);
    console.log("name:", name);

    loginUser.name = name;
    loginUser.uid = uid;
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

    node.exit.on('click', function () {
        document.cookie = 'token=';
        document.cookie = 'uid=';
        document.cookie = 'store_id=';
        location.reload();
    });

    node.usersList.on('click', 'li', function () {
        var _this = $(this),
            uid = _this.attr('data-uid'),
            appid = _this.attr('data-appid'),
            main = $('#main');

        if (customerID == uid && customerAppID == appid) {
            return;
        }
        $('#intro').hide();
        $('#to_user').attr('data-uid', uid);
        $('#to_user').attr('data-appid', appid);

        user = userDB.findUser(appid, uid);
        if (user) {
            $('#to_user').text(helper.getUserName(user));
        }

        if (user.avatar) {
            $('#to_user_avatar').attr("src", helper.getUserAvatar(user));
        } else {
            var defaultAvatar = "static/images/_avatar.png";
            $('#to_user_avatar').attr("src", defaultAvatar);
        }

        main.find('.chat-wrap').removeClass('hide');
        _this.addClass('active').siblings().removeClass('active');
        _this.find('.num').text('');
        ///读取聊天记录添加到列表
        var cid = "" + appid + ":" + uid;
        var messages = imDB.loadUserMessage(cid);
        node.chatHistory.html("");
        for (var i in messages) {
            var msg = messages[i];
            console.log("message:", msg);
            appendMessage(msg);
        }

        customerID = uid;
        customerAppID = appid;
    });

    //deal with chat mode.
    $("#entry").keypress(function (e) {
        if (e.keyCode != 13) return;
        var uid = parseInt($("#to_user").attr("data-uid"));
        var appid = parseInt($("#to_user").attr("data-appid"));
        var msg = $("#entry").val().replace("\n", "");
        if (!util.isBlank(msg)) {
            var now = new Date();
            var obj = {"text": msg};
            var textMsg = JSON.stringify(obj);
            console.log("message text:", textMsg);
            var message = {
                sellerID: loginUser.uid,
                storeID: loginUser.storeID,
                customerID: customerID,
                customerAppID: customerAppID,
                content: textMsg,
                msgLocalID: msgLocalID++,
                outgoing: true,
                timestamp: (now.getTime() / 1000)
            };
            message.contentObj = obj;
            if (im.connectState == IMService.STATE_CONNECTED) {
                var cid = "" + appid + ":" + uid;
                imDB.saveMessage(cid, message);
                im.sendCustomerSupportMessage(message);
                $("#entry").val(""); // clear the entry field.
                addMessage(message);
                $("#chatHistory").show();
            }
        }
        return false;
    });
});




