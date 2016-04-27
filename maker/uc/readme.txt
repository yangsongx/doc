APIs:

[Preface] return code definition:

  code :
    -1 - exception happen
     0 - Successful case
     1 - user already existed in DB

========================================================================
1. /uc/apiCheckExistence/ - 确认用户名是否已存在

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

    $ curl --request POST -d '{"name":"hello"}' "192.168.4.245:9001/uc/apiCheckExistence/"
    $ {"code": 0}

========================================================================
2. /uc/changePwd/ - 修改用户密码
TODO - 根据前端设计的方便，决定使用FORM还是JSON格式
Sample:

========================================================================
3. /uc/forgetPwd/ - 用户忘记密码
TODO - 根据前端设计的方便，决定使用FORM还是JSON格式

========================================================================
4. /uc/apiListRobot/ - 列举出当前用户下的robot

HTTP POST, JSON格式

Req:
  {
      "userid":100
  }

Response:
  {
      "code": 0,
      "list" :[ {...}, {...} ]
  }

Sample:

    $ curl --request POST -d '{"userid":100}' "192.168.4.245:9001/uc/apiListRobot/"
    $ {
        "code": 0,
        "list":
            [
              {"index":1,"name":"hello1" },
              {"index":2,"name":"hello2" },
            ]
      }

========================================================================
5. /uc/apiDelRobot/ - 删除当前用户下的robot

HTTP POST, JSON格式

Req:
  {
      "userid":100,
      "robid":102
  }

Response:
  {
      "code": 0,
  }

Sample:

    $ curl --request POST -d '{"userid":100, "robid":102}' "192.168.4.245:9001/uc/apiDelRobot/"
    $ {
        "code": 0,
      }

========================================================================
6. /uc/apiListCustCorpus/ - 列举所有corpus数据

HTTP POST, JSON格式

Req:
  {
      "userid":100,
  }

Response:
  {
      "code": 0,
      "list": [ ALL CORPUS LIST]
  }

Sample:

    $ curl --request POST -d '{"userid":100}' "192.168.4.245:9001/uc/apiListCustCorpus/"
    $ {
        "code": 0,
        "list":
            [
              {"index" : 1
               "q":"how to ...",
               "a":"you should .."},
              {"index" : 2
               "q":"how to ...",
               "a":"you should .."}
            ]
      }

