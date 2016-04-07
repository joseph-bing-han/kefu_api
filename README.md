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
