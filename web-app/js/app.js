angular.module('MainApp', []).controller('DevicesController', function ($scope, $http) {
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
            (function (response) {
                console.log(response.data);
                $scope.ret.push({ret: response.data["ret"], name: name, number: number});
            });
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
    }
);