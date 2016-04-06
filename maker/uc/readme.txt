APIs:

========================================================================
1. /uc/checkExistence/ - 确认用户名是否已存在

HTTP POST, JSON格式

Req:
  {
      "name":"user name"
  }

Response:
  {
      "code": 0,
      "msg" : "extra error msg"
  }
  code :
    -1 - exception happen
     0 - user is not existed in DB
     1 - user already existed in DB



Sample:

    $ curl --request POST -d '{"name":"hello"}' "192.168.4.245:9001/uc/checkExistence/"
    $ {"code": 0}

========================================================================
2. /uc/changePwd/ - 修改用户密码
TODO - 根据前端设计的方便，决定使用FORM还是JSON格式
Sample:

========================================================================
3. /uc/forgetPwd/ - 用户忘记密码
TODO - 根据前端设计的方便，决定使用FORM还是JSON格式
