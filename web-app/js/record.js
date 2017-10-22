angular.module('Record', []).controller('RecordController', function ($scope, $http) {
    $scope.ips = [];
    $scope.getips = function () {
        $http.get(API_URL + '/record').then(function (response) {
            $scope.ips = response.data;
            })
    };

    $scope.getips();

});