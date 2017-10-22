var app = angular.module('MainApp', []);

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


app.controller('DevicesController', function ($scope, $http, locals) {
        $scope.devices = [];
        $scope.ret = [];
        $scope.refresh = function () {
            $http({
                method: 'GET',
                url: API_URL + "/states",

            }).then(function SuccessfulCallBack(response) {
                $scope.devices = response.data;
                $scope.devices.forEach(function (t) {
                    t["SelectNumber"] = 0
                });
            });
        };

        $scope.refresh();

        $scope.Subscribe = function (name, number) {
            if (number === 0) {
                return;
            }
            $http.post(API_URL + "/device/subscribe", {"DeviceName": name, "SubscribeNumber": number}).then
            (
                function (response) {
                    console.log(response.data);
                    $scope.ret.push({ret: response.data["ret"], name: name, number: number});
                }
            );
            //$scope.refresh();
        };

        $scope.Sub = function (device) {
            if (device["SelectNumber"] > 0) {
                var index = $scope.devices.indexOf(device);
                $scope.devices[index]["SelectNumber"] -= 1;
            }

        };
        $scope.Plus = function (device) {
            if (device["SelectNumber"] < device["RemainingNumber"]) {
                var index = $scope.devices.indexOf(device);
                $scope.devices[index]["SelectNumber"] += 1;
            }
        };
        if (!locals.get('access')) {
            locals.set('access', true);
            $.getJSON("https://api.ip.sb/geoip",
                function (json) {
                    $http.post(API_URL + '/record', json);
                }
            );
        }
        // $http.get("https://api.ip.sb/jsonip").then(function (response) {
        //     $http.post(API_URL + '/record', response.data);
        // })
    }
);


app.controller('RecordController', function ($scope, $http) {
    $scope.ips = [];
    getips = function () {
        $http.get(API_URL + '/record').then(function (response) {
            $scope.ips = response.data;
        })
    };

    getips();

});

app.controller('SignInController', function ($scope, $http, locals) {

    if (locals.get('username') && locals.get('password')) {
        $scope.username = locals.get('username');
        $scope.password = locals.get('password');
        $scope.keep = locals.get('keep');
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
                    locals.set('username', $scope.username);
                    locals.set('password', $scope.password);
                    locals.set('keep', $scope.keep);
                }
                locals.set('token', response.data.token);
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
                        console.log(response.data)
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