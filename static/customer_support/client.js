var loginUser = {};

//当前会话的uid
var customerID = 0;
var customerAppID = 0;

var msgLocalID = 1;
var imDB = new IMDB();

var IMService = gobelieve.IMService;

var userDB = {
    users : new Array(),
    addUser : function(newUser) {
        var exists = false;
        for (var i in this.users) {
            var user = this.users[i];
            if (user.uid == newUser.uid && user.appid == newUser.appid) {
                exists = true;
            }
        }
        if (!exists) {
            this.users.push(newUser);
        }    
        return !exists;
    },
    findUser : function(appid, uid) {
        for (var i in this.users) {
            var user = this.users[i];
            if (user.uid == uid && user.appid == appid) {
                return user;
            }
        }
        return null;
    }
}

var observer = {

    handleCustomerMessage: function(msg, tip) {
        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }
        msg.outgoing = false;
        var user = userDB.findUser(msg.customerAppID, msg.customerID)
        if (!user) {
            user = {uid:msg.customerID, appid:msg.customerAppID}
            userDB.addUser(user);
            addUser(user);

            var url =  "customers/" + msg.customerAppID + "/" + msg.customerID;
            $.ajax({
                url: url,
                dataType: 'json',
                success: function (result, status, xhr) {
                    console.log("customer:", result);
                    if (result['name']) {
                        user.name = result['name'];
                        setUserName(msg.customerAppID, msg.customerID, 
                                    user.name);
                    }
                },
                error: function (xhr, err) {
                    console.log("get customer name err:", err, xhr.status);
                }
            });

        }

        var cid = "" + msg.customerAppID + ":" + msg.customerID;
        imDB.saveMessage(cid, msg);

        if (msg.customerAppID == customerAppID && 
            msg.customerID == customerID) {
            addMessage(msg);
        } else if (tip === undefined || tip) {
            process.msgTip(msg.customerAppID, msg.customerID);
        } 
    },
    handleCustomerSupportMessage: function(msg) {
        if (msg.sellerID != loginUser.uid) {
            return;
        }

        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }
        msg.outgoing = true;
        var user = userDB.findUser(msg.customerAppID, msg.customerID)
        if (!user) {
            user = {uid:msg.customerID, appid:msg.customerAppID}
            userDB.addUser(user)
        }

        var cid = "" + msg.customerAppID + ":" + msg.customerID;
        imDB.saveMessage(cid, msg);
        if (msg.customerAppID == customerAppID && 
            msg.customerID == customerID) {
            addMessage(msg);
        }
    },

    handleCustomerMessageACK: function(msg) {
        console.log("handleCustomerMessageACK msg id:", msg.msgLocalID);
        var cid = "" + msg.customerAppID + ":" + msg.customerID;
        
        var msgLocalID = msg.msgLocalID;
        if (msg.customerAppID == customerAppID && 
            msg.customerID == customerID) {
            process.msgACK(msgLocalID);
        }
        imDB.ackMessage(cid, msgLocalID);
    },

    handleCustomerMessageFailure: function(msg) {
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

var im = new IMService();
im.observer = observer;

