var app = angular.module('MainApp', ["ngCookies"]);

app.factory('locals', ['$window', function ($window) {
    return {        //存储单个属性
        set: function (key, value) {
            $window.localStorage[key] = value;
        },        //读取单个属性
        get: function (key, defaultValue) {
            return $window.localStorage[key] || defaultValue;
        },        //存储对象，以JSON格式存储
        setObject: function (key, value) {
            $window.localStorage[key] = JSON.stringify(value);//将对象以字符串保存
        },        //读取对象
        getObject: function (key) {
            return JSON.parse($window.localStorage[key] || '{}');//获取字符串并解析成对象
        }

    }
}]);


app.controller('DevicesController', function ($scope, $http, $cookieStore) {
        //可以订购的零件信息
        $scope.devices = [];
        //订单提示信息
        $scope.messages = [];
        //如果检测到已经登录，直接使用用户信息
        if ($cookieStore.get('user')) {
            //用户是否登录
            $scope.login = true;
            $scope.username = $cookieStore.get('user').username;
        }
        else {
            $scope.login = false;
        }
        //刷新零件信息
        $scope.refresh = function () {
            $http({
                method: 'GET',
                url: API_URL + "/states"

            }).then(function SuccessfulCallBack(response) {
                $scope.devices = response.data;
                $scope.devices.forEach(function (t) {
                    t["SelectNumber"] = 0
                });
            });
        };

        //订购
        $scope.Subscribe = function (name, number) {
            if (number === 0) {
                return;
            }
            if (!$cookieStore.get('user')) {
                alert('请先登录后再进行操作!');
                return;
            }
            $http.post(API_URL + "/device/subscribe", {
                "DeviceName": name,
                "SubscribeNumber": number,
                'token': $cookieStore.get('token')
            }).then
            (
                function (response) {
                    console.log(response.data);
                    $scope.messages.push({ret: response.data.ret, name: name, number: number});
                }
            );
            //$scope.refresh();
        };
        //减少订购数量
        $scope.Sub = function (device) {
            if (device["SelectNumber"] > 0) {
                var index = $scope.devices.indexOf(device);
                $scope.devices[index]["SelectNumber"] -= 1;
            }

        };
        //增加订购数量
        $scope.Plus = function (device) {
            if (device["SelectNumber"] < device["RemainingNumber"]) {
                var index = $scope.devices.indexOf(device);
                $scope.devices[index]["SelectNumber"] += 1;
            }
        };
        // if (!$cookieStore.get('access')) {
        //     $cookieStore.put('access', true);
        //     $http.get("https://api.ip.sb/geoip").then(function (response) {
        //         $http.post(API_URL + '/record', response.data);
        //     });
        // }
        // else {
        //     $http.get("https://api.ip.sb/geoip").then(function (response) {
        //         $http.post(API_URL + '/record', response.data);
        //     })
        // }
        // if (!$cookies.get('access')) {
        //     $cookies.put('access', true);
        //     $.getJSON("https://api.ip.sb/geoip",
        //         function (json) {
        //             $http.post(API_URL + '/record', json);
        //         }
        //     );
        // }
        //第一次打开页面，直接刷新零件信息
        $scope.refresh();
        //统计访问者信息
        $http.get("https://api.ip.sb/geoip").then(function (response) {
            $http.post(API_URL + '/record/ip', response.data);
        })
    }
);


app.controller('RecordController', function ($scope, $http, $cookieStore) {
    $scope.ips = [];
    var token = $cookieStore.get('token');
    if (!token) {
        alert('你没有访问此页面的权限');
        return;
    }
    getips = function () {
        $http.get(API_URL + '/record/ip' + '?token=' + token).then(function (response) {
                $scope.ips = response.data;
            }, function () {
                alert('你的用户权限不足')
            }
        )
    };
    getips();

});


app.controller('SignInController', function ($scope, $http, $cookieStore) {

    if ($cookieStore.get('user')) {
        var user = $cookieStore.get('user');
        $scope.username = user.username;
        $scope.keep = user.keep;
        if (user.keep)
            $scope.password = user.password;
    }


    $scope.signin = function () {
        $http.post(API_URL + '/user/signin',
            {
                "username": $scope.username,
                "password": $scope.password
            }).then(function (response) {
            console.log(response.data);
            if (response.data.ret === 0) {
                if ($scope.keep) {
                    $cookieStore.put('user',
                        {
                            username: $scope.username,
                            password: $scope.password,
                            keep: $scope.keep
                        }
                    );
                }
                else {
                    $cookieStore.put('user',
                        {
                            username: $scope.username,
                            keep: $scope.keep
                        }
                    );
                }
                $cookieStore.put('token', response.data.token);
                window.location = './index.html';
            }
            else {
                alert('登录失败,请检查用户名和密码');
            }
        })
    }
});

app.controller('SignUpController', function ($scope, $http) {
    $scope.signup = function () {
        if ($scope.username && $scope.password1 && $scope.password2 && $scope.emailadd) {
            if ($scope.password1 === $scope.password2) {
                $http.post(API_URL + '/user/signup',
                    {
                        "username": $scope.username,
                        "password": $scope.password1,
                        "email": $scope.emailadd
                    }).then(
                    function (response) {
                        console.log(response.data);
                        if (response.data.ret === 0) {
                            alert('注册成功');
                            window.location.href = '/signin.html';
                        } else {
                            alert('未知错误')
                        }

                    }
                )
            }
            else {
                alert('密码不一致')
            }
        }
        else {
            alert('请填写完整')
        }
    }

});

// app.controller('OrderController', function ($scope, $http) {
//
//
// });

app.controller('UserController', function ($scope, $http, $cookieStore) {
    if ($cookieStore.get('user')) {
        //用户是否登录
        $scope.login = true;
        $scope.username = $cookieStore.get('user').username;
    }
    $http.get(API_URL + '/user/info/' + $scope.username).then(function (response) {
        console.log(response.data);
        if (!response.data.money) {
            $scope.money = 0;
        }
        else {
            $scope.money = response.data.money;
        }
        $scope.emailadd = response.data.email;

        if (response.data.authority === 'user') {
            $scope.auth = '普通用户';
        }
        else {
            $scope.auth = '管理员';
        }

        $scope.orders = response.data.orders;
    })


});