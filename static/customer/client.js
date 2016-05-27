var loginUser = {};


//当前会话的storeID
var storeID = 0;
var sellerID = 0;

var msgLocalID = 1;

var imDB = new IMDB();

var storeDB = {
    stores : new Array(),
    addStore : function(newStore) {
        var exists = false;
        s = this.findStore(newStore.id);
        if(!s) {
            this.stores.push(newStore);
        }
        return !s;
    },
    findStore : function(storeID) {
        for (var i in this.stores) {
            var store = this.stores[i];
            if (store.id == storeID) {
                return store;
            }
        }
        return null;
    }
}

var messageObserver = {
    handleCustomerMessage: function(msg) {
        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }
        msg.outgoing = true;
        var store = storeDB.findStore(msg.storeID);
        if (!store) {
            store = {id:msg.storeID}
            storeDB.addStore(store);
            addStore(store);
        }

        if (!store.name) {
            var url =  "/stores/" + msg.storeID;
            $.ajax({
                url: url,
                dataType: 'json',
                success: function (result, status, xhr) {
                    console.log("customer:", result);
                    if (result['name']) {
                        store.name = result['name'];
                        setUserName(msg.storeID,
                                    store.name);
                    }
                },
                error: function (xhr, err) {
                    console.log("get customer name err:", err, xhr.status);
                }
            });
        }

        imDB.saveMessage(msg.storeID, msg);

        if (msg.storeID == storeID) {
            addMessage(msg);
        }
    },

    handleCustomerSupportMessage: function(msg, tip) {
        try {
            msg.contentObj = JSON.parse(msg.content)
        } catch (e) {
            console.log("json parse exception:", e);
            return
        }
        msg.outgoing = false;
        var store = storeDB.findStore(msg.storeID);
        if (!store) {
            store = {id:msg.storeID};
            storeDB.addStore(store)
        }

        imDB.saveMessage(msg.storeID, msg);
        if (msg.storeID == storeID) {
            addMessage(msg);
            sellerID = msg.sellerID;
        } else if (tip === undefined || tip) {
            process.msgTip(msg.storeID);
        } 
    },

    handleCustomerMessageACK: function(msg) {
        console.log("handleCustomerMessageACK...");
        var msgLocalID = msg.msgLocalID;
        if (msg.storeID == storeID) {
            process.msgACK(msgLocalID);
        }
        imDB.ackMessage(msg.storeID, msgLocalID);
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

var im = new IMService(messageObserver);

