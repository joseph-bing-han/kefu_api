gobelieve客服api
===============



###客服登录
- 请求地址：**POST /auth/token**
- 请求内容:

        {
            "username":"用户名(email地址)",
            "password":"密码",
        }
        
- 成功响应:

		{
            "access_token":"访问token",
            "refresh_token":"刷新token",
            "expires_in":"过期时间 单位秒",
            "user_id":"用户id"
		}

- 操作失败:
  400



### 刷新access_token
- 请求地址：**POST /auth/refresh_token**
- 是否认证：是
- 请求内容:

        {
            "refresh_token":"刷新token"
        }
    
- 成功响应:

		{
			"access_token":"访问token",
			"refresh_token":"刷新token",
			"expires_in":"过期时间 单位秒",
		}

- 操作失败:
  400



##客服页面地址
'http://k.gobelieve.io/chat/pc/index.html?store=xx&appid=xx&uid=xx&token=xx'
其中appid,uid,token是可选的,如果未提供则会临时生成匿名用户

##客服接入


        <script>
            (function () {
                var btn = document.createElement("button");
                btn.style.position = 'fixed';
                btn.style.bottom = 0;
                btn.style.right = 0;
                btn.setAttribute('id', 'openMessage');
                btn.appendChild(document.createTextNode('联系客服'));
                document.body.appendChild(btn);
                document.getElementById('openMessage').onclick = function () {
                    var a = 'http://k.gobelieve.io/chat/pc/index.html?store=62',
                        o = "_blank",
                        t = "height=600, width=500, top=50, left=50, toolbar=no, menubar=no, scrollbars=no, resizable=no, status=no";
                    console.log(a)
                    window.open(a, o, t)
                };
            }());

        </script>
