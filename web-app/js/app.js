angular.module('MyApp', []).controller('DevicesController', function ($scope, $http) {
        $scope.devices = [];
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

            $http.post(API_URL + "/device/subscribe", {"DeviceName": name, "SubscribeNumber": number}).then
            (function (response) {
                console.log(response.data);
                if(response.data["ret"] == 0)
                {
                    $scope.submit_success = true;
                }
                else
                {
                    $scope.submit_success = false;
                }
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